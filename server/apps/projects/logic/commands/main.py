from apps.projects.logic.commands import project, project_asset

COMMANDS = (
    (
        project_asset.upload_figma.Command,
        project_asset.upload_figma.CommandHandler,
    ),
    (
        project_asset.upload_image.Command,
        project_asset.upload_image.CommandHandler,
    ),
    (
        project.delete.Command,
        project.delete.CommandHandler,
    ),
    (
        project.update.Command,
        project.update.CommandHandler,
    ),
    (
        project.create.Command,
        project.create.CommandHandler,
    ),
)
