import logging
from pkg_resources import WorkingSet, Environment, load_entry_point


def load_plugins(plugin_dir_list):
    working_set = WorkingSet()
    plugin_dists, errors = working_set.find_plugins(
        Environment(plugin_dir_list))
    logging.error(f'Error while loading: {errors}')
    return plugin_dists


def get_entry_points(plugin_dists):
    for dist in plugin_dists:
        try:
            load_entry_point(dist)
        except ImportError:
            logging.error(f'Error while getting {dist} entry point')
