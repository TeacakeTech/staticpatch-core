# Continuous Deployment (CD) with GitLab

This is a guide, edit as needed. You can use any static site builder you can get to run in GitLab - which should be pretty much any of them!

## Live builds

In "CI/CD" setting, set the following variables with "Expand variable reference" flag off:

* `STATICPATCH_DOMAIN` - domain of the StaticPatch app to push to ("Protect variable" off)
* `STATICPATCH_SITE` - slug of the site you want to push to ("Protect variable" off)
* `STATICPATCH_SECURITY_KEY` - a security key for that site ("Protect variable" on)

Add the following files:


`.gitlab-ci.yml`:

```
include:
  - local: .gitlab-ci.main.yml
    rules:
      - if: $CI_COMMIT_BRANCH == "main"
```

`.gitlab-ci.main.yml`:

```
image: python:3.13

stages:
 - deploy


deploy-main:
  stage: deploy
  script: 
    - pip install staticpipes
    - python staticpipes.py build
    - apt-get update
    - apt-get install zip
    - cd _site && zip -r out.zip * 
    - "curl --retry 10 --retry-delay 30 --retry-all-errors -X POST \"https://$STATICPATCH_DOMAIN/api/site/$STATICPATCH_SITE/publish_built_site\"  -H  \"Content-Type: multipart/form-data\" -H \"Security-Key: $STATICPATCH_SECURITY_KEY\" -F \"built_site=@\\\"out.zip\\\"\"" 
  environment: production
```

## Preview builds

You'll need the variables from the previous step.

In "CI/CD" setting, add the following variables with "Expand variable reference" flag off:

* `STATICPATCH_PREVIEW` - slug of the preview type you want to send previews to ("Protect variable" off)

Change `.gitlab-ci.yml` to :

```
include:
  - local: .gitlab-ci.main.yml
    rules:
      - if: $CI_COMMIT_BRANCH == "main"
  - local: .gitlab-ci.dev.yml
    rules:
      - if: $CI_COMMIT_BRANCH != "main"
```

Add `.gitlab-ci.dev.yml`:

```
image: python:3.13

stages:
 - deploy-dev


deploy-dev:
  stage: deploy-dev
  script: 
    - pip install staticpipes
    - python staticpipes.py build
    - apt-get update
    - apt-get install zip
    - cd _site && zip -r out.zip * 
    - "curl --retry 10 --retry-delay 30 --retry-all-errors -X POST \"https://$STATICPATCH_DOMAIN/api/site/$STATICPATCH_SITE/preview/$STATICPATCH_PREVIEW/instance/$CI_COMMIT_BRANCH/publish_built_site\"  -H  \"Content-Type: multipart/form-data\" -H \"Security-Key: $STATICPATCH_SECURITY_KEY\" -F \"built_site=@\\\"out.zip\\\"\"" 
  environment:
    name: branch/$CI_COMMIT_BRANCH
    url: https://$CI_COMMIT_BRANCH.preview.secondguessing.net
    on_stop: remove-dev


remove-dev:
  stage: deploy-dev
  variables:
    GIT_STRATEGY: none
  script:
    - "curl --retry 10 --retry-delay 30 --retry-all-errors -X POST \"https://$STATICPATCH_DOMAIN/api/site/$STATICPATCH_SITE/preview/$STATICPATCH_PREVIEW/instance/$CI_COMMIT_BRANCH/deactivate\"  -H \"Security-Key: $STATICPATCH_SECURITY_KEY\""
  when: manual
  environment:
    name: branch/$CI_COMMIT_BRANCH
    action: stop 
```
