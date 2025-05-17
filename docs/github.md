# Continuous Deployment (CD) with GitHub Actions

This is a guide, edit as needed. You can use any static site builder you can get to run in GitHub - which should be pretty much any of them!

## Live builds

In "Secrets and Variables", "Actions", add the following variables:

* `STATICPATCH_DOMAIN` - domain of the StaticPatch app to push to
* `STATICPATCH_PUBLIC_SITE` - slug of the site you want to push to

And add the `STATICPATCH_PUBLIC_SECURITY_KEY` secret.

Add the following files:

`.github/workflows/live-deploy.yml`:

```
name: Live Deploy
on: [push]

jobs:
  live-deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
      with:
        submodules: recursive
        fetch-depth: 0
    - name: Setup python
      uses: actions/setup-python@v5
      with:
        python-version: 3.13
        architecture: x64
    - name: Install Software
      run: pip install staticpatch
    - name: Make site
      run: python site.py build
    - name: Zip site
      run: zip -r out.zip *
      working-directory: ./_site
    - name: Upload Site
      run: "curl --retry 10 --retry-delay 30 --retry-all-errors -X POST \"https://${{ vars.STATICPATCH_DOMAIN }}/api/site/${{ vars.STATICPATCH_PUBLIC_SITE }}/publish_built_site\"  -H  \"Content-Type: multipart/form-data\" -H \"Security-Key: ${{ secrets.STATICPATCH_PUBLIC_SECURITY_KEY }}\" -F \"built_site=@\\\"out.zip\\\"\""
      working-directory: ./_site
```

## Preview builds

You'll need the secrets and variables from the previous step.

In "Secrets and Variables", "Actions", add the following variables:

* `STATICPATCH_PREVIEW`- slug of the preview type you want to send previews to

Add the following files:

`.github/workflows/preview-deploy.yml`:

```
name: Preview Deploy
on: [push]

jobs:
  preview-deploy:
    runs-on: ubuntu-latest
    if: github.ref != 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
      with:
        submodules: recursive
        fetch-depth: 0
    - name: Setup python
      uses: actions/setup-python@v5
      with:
        python-version: 3.13
        architecture: x64
    - name: Install Software
      run: pip install staticpatch
    - name: Make site
      run: python site.py build
    - name: Zip site
      run: zip -r out.zip *
      working-directory: ./_site
    - name: Upload Site
      run: "curl --retry 10 --retry-delay 30 --retry-all-errors -X POST \"https://${{ vars.STATICPATCH_DOMAIN }}/api/site/${{ vars.STATICPATCH_PUBLIC_SITE }}/preview/${{ vars.STATICPATCH_PREVIEW }}/instance/${GITHUB_HEAD_REF:-${GITHUB_REF#refs/heads/}}/publish_built_site\"  -H  \"Content-Type: multipart/form-data\" -H \"Security-Key: ${{ secrets.STATICPATCH_PUBLIC_SECURITY_KEY }}\" -F \"built_site=@\\\"out.zip\\\"\""
      working-directory: ./_site
```

`.github/workflows/preview-delete.yml`:

```
name: Preview Delete
on: delete

jobs:
  preview-delete:
    runs-on: ubuntu-latest
    if: github.event.ref_type == 'branch' && github.event.ref != 'refs/heads/main'
    steps:
    - name: Deactivate Site
      run: "curl --retry 10 --retry-delay 30 --retry-all-errors -X POST \"https://${{ vars.STATICPATCH_DOMAIN }}/api/site/${{ vars.STATICPATCH_PUBLIC_SITE }}/preview/${{ vars.STATICPATCH_PREVIEW }}/instance/${{ github.event.ref }}/deactivate\" -H \"Security-Key: ${{ secrets.STATICPATCH_PUBLIC_SECURITY_KEY }}\" "
```

