

import pathlib
import sys
import click
import traceback
import tempfile

from honeybee_vtk.model import Model
from honeybee_vtk.vtkjs.schema import SensorGridOptions, DisplayMode
from honeybee_vtk.types import ImageTypes
from honeybee_vtk.text_actor import TextActor
from honeybee_vtk.timestep_images import export_timestep_images, _extract_periods_colors


@click.group()
def export():
    """Export images of an HBJSON file."""
    pass


@export.command('model-images')
@click.argument('hbjson-file')
@click.option(
    '--folder', '-f', help='Path to target folder.',
    type=click.Path(exists=False, file_okay=False, resolve_path=True,
                    dir_okay=True), default='.', show_default=True
)
@click.option(
    '--image-type', '-it', type=click.Choice(['png', 'jpg', 'ps', 'tiff', 'bmp', 'pnm'],
                                             case_sensitive=False), default='jpg',
    help='choose the type of image file.', show_default=True
)
@click.option(
    '--image-width', '-iw', type=int, default=0, help='Width of images in pixels.'
    ' If not set, Radiance default x dimension of view will be used.', show_default=True
)
@click.option(
    '--image-height', '-ih', type=int, default=0, help='Height of images in pixels.'
    'If not set, Radiance default y dimension of view will be used.', show_default=True
)
@click.option(
    '--background-color', '-bc', type=(int, int, int), default=(255, 255, 255),
    help='Set background color for images', show_default=True
)
@click.option(
    '--model-display-mode', '-mdm',
    type=click.Choice(['shaded', 'surface', 'surfacewithedges', 'wireframe', 'points'],
                      case_sensitive=False),
    default='shaded', help='Set display mode for the model.', show_default=True
)
@click.option(
    '--grid-options', '-go',
    type=click.Choice(['ignore', 'points', 'meshes'], case_sensitive=False),
    default='ignore', help='Export sensor grids as either points or meshes.',
    show_default=True,
)
@click.option(
    '--grid-display-mode', '-gdm',
    type=click.Choice(['shaded', 'surface', 'surfacewithedges',
                       'wireframe', 'points'], case_sensitive=False),
    default='shaded', help='Set display mode for the Sensorgrids.',
    show_default=True
)
@click.option(
    '--view', '-vf', help='File Path to the Radiance view file. Multiple view files are'
    ' accepted.', type=click.Path(exists=True), default=None,
    show_default=True, multiple=True
)
@click.option(
    '--config', '-cf', help='File Path to the config json file which can be used to'
    ' mount simulation data on HBJSON.', type=click.Path(exists=True), default=None,
    show_default=True
)
@click.option(
    '--validate-data', '-vd', is_flag=True, default=False,
    help='Validate simulation data before loading on the model. This is recommended'
    ' when using this command locally.', show_default=True
)
def export_model_images(
        hbjson_file, folder, image_type, image_width, image_height,
        background_color, model_display_mode, grid_options, grid_display_mode, view, config, validate_data,):
    """Export images of the Honeybee Model created from the HBJSON file.

    \b
    Args:
        hbjson-file: Path to an HBJSON file.

    """
    folder = pathlib.Path(folder)
    folder.mkdir(exist_ok=True, parents=True)

    if image_type.lower() == 'png':
        image_type = ImageTypes.png
    elif image_type.lower() == 'jpg':
        image_type = ImageTypes.jpg
    elif image_type.lower() == 'ps':
        image_type == ImageTypes.ps
    elif image_type.lower() == 'tiff':
        image_type == ImageTypes.tiff
    elif image_type.lower() == 'bmp':
        image_type == ImageTypes.bmp
    elif image_type.lower() == 'pnm':
        image_type == ImageTypes.pnm

    if grid_options.lower() == 'ignore':
        grid_option = SensorGridOptions.Ignore
    elif grid_options.lower() == 'points':
        grid_option = SensorGridOptions.Sensors
    elif grid_options.lower() == 'meshes':
        grid_option = SensorGridOptions.Mesh

    if model_display_mode.lower() == 'shaded':
        model_display_mode = DisplayMode.Shaded
    elif model_display_mode.lower() == 'surface':
        model_display_mode = DisplayMode.Surface
    elif model_display_mode.lower() == 'surfacewithedges':
        model_display_mode = DisplayMode.SurfaceWithEdges
    elif model_display_mode.lower() == 'wireframe':
        model_display_mode = DisplayMode.Wireframe
    elif model_display_mode.lower() == 'points':
        model_display_mode = DisplayMode.Points

    if grid_display_mode.lower() == 'shaded':
        grid_display_mode = DisplayMode.Shaded
    elif grid_display_mode.lower() == 'surface':
        grid_display_mode = DisplayMode.Surface
    elif grid_display_mode.lower() == 'surfacewithedges':
        grid_display_mode = DisplayMode.SurfaceWithEdges
    elif grid_display_mode.lower() == 'wireframe':
        grid_display_mode = DisplayMode.Wireframe
    elif grid_display_mode.lower() == 'points':
        grid_display_mode = DisplayMode.Points

    try:
        model = Model.from_hbjson(hbjson=hbjson_file, load_grids=grid_option)

        output = model.to_images(
            folder=folder.as_posix(),
            config=config,
            validation=validate_data,
            model_display_mode=model_display_mode,
            grid_display_mode=grid_display_mode,
            background_color=background_color,
            view=view,
            image_type=image_type,
            image_width=image_width,
            image_height=image_height,)

    except Exception:
        traceback.print_exc()
        sys.exit(1)
    else:
        print(f'Success: {output}', file=sys.stderr)
        return sys.exit(0)


@export.command('grid-images')
@click.argument('hbjson-file')
@click.option(
    '--folder', '-f', help='Path to target folder.',
    type=click.Path(exists=False, file_okay=False, resolve_path=True,
                    dir_okay=True), default='.', show_default=True
)
@click.option(
    '--image-type', '-it', type=click.Choice(['png', 'jpg', 'ps', 'tiff', 'bmp', 'pnm'],
                                             case_sensitive=False), default='jpg',
    help='choose the type of image file.', show_default=True
)
@click.option(
    '--image-width', '-iw', type=int, default=0, help='Width of images in pixels.'
    ' If not set, Radiance default x dimension of view will be used.', show_default=True
)
@click.option(
    '--image-height', '-ih', type=int, default=0, help='Height of images in pixels.'
    'If not set, Radiance default y dimension of view will be used.', show_default=True
)
@click.option(
    '--background-color', '-bc', type=(int, int, int), default=(255, 255, 255),
    help='Set background color for images', show_default=True
)
@click.option(
    '--grid-options', '-go',
    type=click.Choice(['ignore', 'points', 'meshes'], case_sensitive=False),
    default='ignore', help='Export sensor grids as either points or meshes.',
    show_default=True,
)
@click.option(
    '--grid-display-mode', '-gdm',
    type=click.Choice(['shaded', 'surface', 'surfacewithedges',
                       'wireframe', 'points'], case_sensitive=False),
    default='shaded', help='Set display mode for the Sensorgrids.',
    show_default=True
)
@click.option(
    '--config', '-cf', help='File Path to the config json file which can be used to'
    ' mount simulation data on HBJSON.', type=click.Path(exists=True), default=None,
    show_default=True
)
@click.option(
    '--grids-filter', '-gf', type=str, default='*', show_default=True, multiple=True,
    help='A regex pattern as a string to filter the grids. Defaults to *'
    ' which will export all the grids.'
)
@click.option(
    '--full-match/--no-full-match', help='Flag to note whether the grids'
    ' should be filtered by their identifiers as full matches.', default=False, show_default=True, is_flag=True
)
@click.option(
    '--text-content', type=str, default=None, show_default=True, help='Text to be '
    'displayed on an image of a grid. This will put this same text on all of the images.'
)
@click.option(
    '--text-height', '-th', type=int, default=15, show_default=True,
    help='Set the height of the text in pixels for the text that will be added to the'
    ' image of a grid.'
)
@click.option(
    '--text-color', '-tc', type=(int, int, int), default=(0, 0, 0), show_default=True,
    help='Set the text color of the text that will added to the image of a grid.'
)
@click.option(
    '--text-position', '-tp', type=(float, float), default=(0.5, 0.0), show_default=True,
    help='Set the text position of the text to added to the image of a grid. The setting'
    ' is applied at the lower left point of the text. (0,0) will give you the lower'
    ' left corner of the image. (1,1) will give you the upper right corner of the image.'
)
@click.option(
    '--text-bold/--text-normal', is_flag=True, default=False, show_default=True,
    help='Set the text to be bold for the text that will added to the image of a grid.'
)
def export_grid_images(
        hbjson_file, folder, image_type, image_width, image_height,
        background_color, grid_options, grid_display_mode,
        config, grids_filter, full_match, text_content, text_height, text_color,
        text_position, text_bold):
    """Export images of the grids for the Honeybee Model created from the HBJSON file.

    \b
    Args:
        hbjson-file: Path to an HBJSON file.

    """
    folder = pathlib.Path(folder)
    folder.mkdir(exist_ok=True, parents=True)

    if image_type.lower() == 'png':
        image_type = ImageTypes.png
    elif image_type.lower() == 'jpg':
        image_type = ImageTypes.jpg
    elif image_type.lower() == 'ps':
        image_type == ImageTypes.ps
    elif image_type.lower() == 'tiff':
        image_type == ImageTypes.tiff
    elif image_type.lower() == 'bmp':
        image_type == ImageTypes.bmp
    elif image_type.lower() == 'pnm':
        image_type == ImageTypes.pnm

    if grid_options.lower() == 'ignore':
        grid_option = SensorGridOptions.Ignore
    elif grid_options.lower() == 'points':
        grid_option = SensorGridOptions.Sensors
    elif grid_options.lower() == 'meshes':
        grid_option = SensorGridOptions.Mesh

    if grid_display_mode.lower() == 'shaded':
        grid_display_mode = DisplayMode.Shaded
    elif grid_display_mode.lower() == 'surface':
        grid_display_mode = DisplayMode.Surface
    elif grid_display_mode.lower() == 'surfacewithedges':
        grid_display_mode = DisplayMode.SurfaceWithEdges
    elif grid_display_mode.lower() == 'wireframe':
        grid_display_mode = DisplayMode.Wireframe
    elif grid_display_mode.lower() == 'points':
        grid_display_mode = DisplayMode.Points

    try:
        model = Model.from_hbjson(hbjson=hbjson_file, load_grids=grid_option)

        text_actor = TextActor(text=text_content, height=text_height, color=text_color,
                               position=text_position, bold=text_bold)\
            if text_content else None

        output = model.to_grid_images(config=config, folder=folder,
                                      grids_filter=grids_filter,
                                      full_match=full_match,
                                      grid_display_mode=grid_display_mode,
                                      background_color=background_color,
                                      image_type=image_type,
                                      image_width=image_width,
                                      image_height=image_height,
                                      text_actor=text_actor)

    except Exception:
        traceback.print_exc()
        sys.exit(1)
    else:
        print(f'Success: {output}', file=sys.stderr)
        return sys.exit(0)


# @export.command('timestep-images')
# @click.argument('hbjson-file')
# @click.option(
#     '--folder', '-f', help='Path to target folder.',
#     type=click.Path(exists=False, file_okay=False, resolve_path=True,
#                     dir_okay=True), default='.', show_default=True
# )
# @click.option(
#     '--image-type', '-it', type=click.Choice(['png', 'jpg', 'ps', 'tiff', 'bmp', 'pnm'],
#                                              case_sensitive=False), default='jpg',
#     help='choose the type of image file.', show_default=True
# )
# @click.option(
#     '--image-width', '-iw', type=int, default=0, help='Width of images in pixels.'
#     ' If not set, Radiance default x dimension of view will be used.', show_default=True
# )
# @click.option(
#     '--image-height', '-ih', type=int, default=0, help='Height of images in pixels.'
#     'If not set, Radiance default y dimension of view will be used.', show_default=True
# )
# @click.option(
#     '--grid-display-mode', '-gdm',
#     type=click.Choice(['shaded', 'surface', 'surfacewithedges',
#                        'wireframe', 'points'], case_sensitive=False),
#     default='shaded', help='Set display mode for the Sensorgrids.',
#     show_default=True
# )
# @click.option(
#     '--config', '-cf', help='File Path to the config json file which can be used to'
#     ' mount simulation data on HBJSON.', type=click.Path(exists=True), default=None,
#     show_default=True
# )
# @click.option(
#     '--grid-filter', '-gf', type=str, default=[], show_default=True, multiple=True,
#     help='Filter sensor grids by name. Use this option multiple times to use multiple'
#     ' grid identifiers as filters.'
# )
# @click.option(
#     '--text-content', type=str, default=None, show_default=True, help='Text to be '
#     'displayed on an image of a grid. This will put this same text on all of the images.'
# )
# @click.option(
#     '--text-height', '-th', type=int, default=15, show_default=True,
#     help='Set the height of the text in pixels for the text that will be added to the'
#     ' image of a grid.'
# )
# @click.option(
#     '--text-color', '-tc', type=(int, int, int), default=(0, 0, 0), show_default=True,
#     help='Set the text color of the text that will added to the image of a grid.'
# )
# @click.option(
#     '--text-position', '-tp', type=(float, float), default=(0.5, 0.0), show_default=True,
#     help='Set the text position of the text to added to the image of a grid. The setting'
#     ' is applied at the lower left point of the text. (0,0) will give you the lower'
#     ' left corner of the image. (1,1) will give you the upper right corner of the image.'
# )
# @click.option(
#     '--text-bold/--text-normal', is_flag=True, default=False, show_default=True,
#     help='Set the text to be bold for the text that will added to the image of a grid.'
# )
# def export_timestep_images(
#         hbjson_file, folder, image_type, image_width, image_height, grid_options,
#         grid_display_mode, config, grid_filter, text_content, text_height, text_color,
#         text_position, text_bold):
#     """Export an image for each time step in data for all or selected grids of the model.

#     \b
#     Args:
#         hbjson-file: Path to an HBJSON file.

#     """
#     folder = pathlib.Path(folder)
#     folder.mkdir(exist_ok=True, parents=True)

#     if image_type.lower() == 'png':
#         image_type = ImageTypes.png
#     elif image_type.lower() == 'jpg':
#         image_type = ImageTypes.jpg
#     elif image_type.lower() == 'ps':
#         image_type == ImageTypes.ps
#     elif image_type.lower() == 'tiff':
#         image_type == ImageTypes.tiff
#     elif image_type.lower() == 'bmp':
#         image_type == ImageTypes.bmp
#     elif image_type.lower() == 'pnm':
#         image_type == ImageTypes.pnm

#     if grid_display_mode.lower() == 'shaded':
#         grid_display_mode = DisplayMode.Shaded
#     elif grid_display_mode.lower() == 'surface':
#         grid_display_mode = DisplayMode.Surface
#     elif grid_display_mode.lower() == 'surfacewithedges':
#         grid_display_mode = DisplayMode.SurfaceWithEdges
#     elif grid_display_mode.lower() == 'wireframe':
#         grid_display_mode = DisplayMode.Wireframe
#     elif grid_display_mode.lower() == 'points':
#         grid_display_mode = DisplayMode.Points

#     try:
#         periods, grid_colors = _extract_periods_colors(periods_file)

#         if not config:
#             raise ValueError('Config file not provided.')
#         if not time_step_file_name:
#             raise ValueError('Time step file name not provided.')
#         if not periods:
#             raise ValueError('Periods file not provided.')

#         if grid_display_mode == DisplayMode.Points:
#             print('Grids as points are not supported for image export of timesteps.')
#             grid_display_mode = DisplayMode.Shaded

#         text_actor = TextActor(text=text_content, height=text_height, color=text_color,
#                                position=text_position, bold=text_bold)\
#             if text_content else None

#         temp_folder = pathlib.Path(tempfile.mkdtemp())
#         output = export_timestep_images(hbjson_path=hbjson_file, config_path=config,
#                                         timestamp_file_name=time_step_file_name,
#                                         periods=periods, grid_colors=grid_colors,
#                                         grid_display_mode=grid_display_mode,
#                                         target_folder=temp_folder,
#                                         grid_filter=grid_filter,
#                                         text_actor=text_actor,
#                                         label_images=False,
#                                         image_type=image_type,
#                                         image_width=image_width,
#                                         image_height=image_height)
#     except Exception:
#         traceback.print_exc()
#         sys.exit(1)
#     else:
#         print(f'Success: {output}', file=sys.stderr)
#         return sys.exit(0)
