import config_data
import global_game_data
import graph_data
import sys


def get_relative_graph_x(absolute_x_value):
    max_x_graph = sys.float_info.min
    min_x_graph = sys.float_info.max
    for graph_point in graph_data.graph_data[global_game_data.current_graph_index]:
        if graph_point[0][0] < min_x_graph:
            min_x_graph = graph_point[0][0]
        if graph_point[0][0] > max_x_graph:
            max_x_graph = graph_point[0][0]
    max_display_width = config_data.window_width - config_data.display_size_left - config_data.display_size_right - 2 \
                        * config_data.graph_padding
    return (absolute_x_value - min_x_graph) * max_display_width / (max_x_graph - min_x_graph) + \
           config_data.graph_padding + config_data.display_size_left


def get_relative_graph_y(absolute_y_value):
    max_y_graph = sys.float_info.min
    min_y_graph = sys.float_info.max
    for graph_point in graph_data.graph_data[global_game_data.current_graph_index]:
        if graph_point[0][1] < min_y_graph:
            min_y_graph = graph_point[0][1]
        if graph_point[0][1] > max_y_graph:
            max_y_graph = graph_point[0][1]
    max_display_height = config_data.window_height - config_data.display_size_top - \
                         config_data.display_size_bottom - 2 * config_data.graph_padding
    return (absolute_y_value - min_y_graph) * max_display_height / (
            max_y_graph - min_y_graph) + config_data.graph_padding + config_data.display_size_bottom


def get_absolute_speed():
    max_x_graph = sys.float_info.min
    min_x_graph = sys.float_info.max
    for graph_point in graph_data.graph_data[global_game_data.current_graph_index]:
        if graph_point[0][0] < min_x_graph:
            min_x_graph = graph_point[0][0]
        if graph_point[0][0] > max_x_graph:
            max_x_graph = graph_point[0][0]
    range_of_x_values = max_x_graph - min_x_graph
    speed_coefficient = 1 / 5
    return config_data.player_speed * range_of_x_values * speed_coefficient
