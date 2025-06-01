import datetime
import os
import zipfile

from django_tasks import task

import staticpatchcore.models
import staticpatchcore.update_server_config


@task()
def process_build_task(build_id: str) -> None:
    build = staticpatchcore.models.BuildModel.objects.get(id=build_id)
    if build.deleted_at:
        return
    print("Processing build {0} for site {1} ({2})".format(build.id, build.site.slug, build.site.id))

    # Start build
    build.started_at = datetime.datetime.now()
    build.save()

    try:

        # Extract Zip
        file_name = os.path.join(
            build.get_full_file_storage_directory(),
            "site.zip",
        )
        out_dir_name = os.path.join(
            build.get_full_file_storage_directory(),
            "out",
        )
        os.makedirs(out_dir_name)
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(out_dir_name)

        # Build done!
        build.finished_at = datetime.datetime.now()
        build.save()

        # Rebuild Apache Conf
        staticpatchcore.update_server_config.update_server_config()

    except Exception as e:
        # build.error = str(e)
        build.failed_at = datetime.datetime.now()
        build.save()
        raise e


@task()
def update_server_config_task() -> None:
    staticpatchcore.update_server_config.update_server_config()
