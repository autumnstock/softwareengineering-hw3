import pyglet

import config_data
import graph_data
import global_game_data
import colors
import relative_display_functions
import pathing


class Graph:
    graph_lines = []
    graph_points = []
    graph_line_coordinates = []
    graph_point_coordinates = []
    display_size_scoreboard = 400
    display_size_bottom_controls = 100
    graph_padding = 60
    target_x = 0
    target_y = 0
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    path_lines = []

    def __init__(self, batch):
        self.batch = batch
        self.group1 = pyglet.graphics.Group(order=1)
        self.group2 = pyglet.graphics.Group(order=2)
        self.group3 = pyglet.graphics.Group(order=3)
        self.group4 = pyglet.graphics.Group(order=4)
        self.group5 = pyglet.graphics.Group(order=5)
        pathing.set_current_graph_paths()
        self.set_up_graph()

        target_image = pyglet.resource.image("target.png")
        self.target = pyglet.sprite.Sprite(img=target_image, x=100, y=100, batch=batch,
                                           group=self.group5)
        self.target.scale_x = 1.2
        self.target.scale_y = 1.2

        start_image = pyglet.resource.image("start.png")
        self.start = pyglet.sprite.Sprite(img=start_image, x=100, y=100, batch=batch,
                                          group=self.group5)

        end_image = pyglet.resource.image("exit.png")
        self.end = pyglet.sprite.Sprite(img=end_image, x=100, y=100, batch=batch,
                                        group=self.group5)

    def set_up_graph(self):
        for graph_line in self.graph_lines:
            graph_line.delete()
        for graph_point in self.graph_points:
            graph_point.delete()
        self.graph_lines.clear()
        self.graph_points.clear()
        self.graph_line_coordinates.clear()
        self.graph_point_coordinates.clear()
        # Draw lines for connections between vertices
        for graph_point in graph_data.graph_data[global_game_data.current_graph_index]:
            for other_point_index in graph_point[1]:
                start_x = graph_point[0][0]
                start_y = graph_point[0][1]
                other_point = graph_data.graph_data[global_game_data.current_graph_index][other_point_index]
                end_x = other_point[0][0]
                end_y = other_point[0][1]
                self.graph_line_coordinates.append((start_x, start_y, end_x, end_y))
                line = pyglet.shapes.Line(start_x, start_y, end_x, end_y,
                                          color=colors.WHITE[colors.SHAPE_INDEX],
                                          thickness=3.0, batch=self.batch, group=self.group1)
                self.graph_lines.append(line)
        # Draw graph points and add labels for each vertex
        for index, graph_point in enumerate(graph_data.graph_data[global_game_data.current_graph_index]):
            x_coordinate = graph_point[0][0]
            y_coordinate = graph_point[0][1]
            self.graph_point_coordinates.append((x_coordinate, y_coordinate))
            outer_circle = pyglet.shapes.Circle(x_coordinate, y_coordinate, 25,
                                                color=colors.YELLOW[colors.SHAPE_INDEX],
                                                batch=self.batch,
                                                group=self.group2)
            self.graph_points.append(outer_circle)
            inner_circle = pyglet.shapes.Circle(x_coordinate, y_coordinate, 20,
                                                color=colors.WHITE[colors.SHAPE_INDEX],
                                                batch=self.batch,
                                                group=self.group3)
            self.graph_points.append(inner_circle)
            circle_label = pyglet.text.Label(str(index), font_name='Arial', font_size=20,
                                             x=x_coordinate, y=y_coordinate,
                                             anchor_x='center', anchor_y='center',
                                             color=colors.BLACK[colors.TEXT_INDEX],
                                             batch=self.batch, group=self.group4)
            self.graph_points.append(circle_label)
            # Set location for target object
            if index == global_game_data.target_node:
                self.target_x = x_coordinate
                self.target_y = y_coordinate
            # Set location for start object
            if index == 0:
                self.start_x = x_coordinate
                self.start_y = y_coordinate
            # Set location for end object
            if index == len(graph_data.graph_data[global_game_data.current_graph_index]) - 1:
                self.end_x = x_coordinate
                self.end_y = y_coordinate

    def resize_graph(self):
        for index, graph_point in enumerate(self.graph_points):
            coordinates = self.graph_point_coordinates[index // 3]
            graph_point.x = relative_display_functions.get_relative_graph_x(coordinates[0])
            graph_point.y = relative_display_functions.get_relative_graph_y(coordinates[1])
        for index, graph_line in enumerate(self.graph_lines):
            coordinates = self.graph_line_coordinates[index]
            graph_line.x = relative_display_functions.get_relative_graph_x(coordinates[0])
            graph_line.y = relative_display_functions.get_relative_graph_y(coordinates[1])
            graph_line.x2 = relative_display_functions.get_relative_graph_x(coordinates[2])
            graph_line.y2 = relative_display_functions.get_relative_graph_y(coordinates[3])
        self.target.x = relative_display_functions.get_relative_graph_x(self.target_x) - self.target.width // 2
        self.target.y = relative_display_functions.get_relative_graph_y(self.target_y) - self.target.height // 2
        self.start.x = relative_display_functions.get_relative_graph_x(self.start_x) - self.start.width // 2
        self.start.y = relative_display_functions.get_relative_graph_y(self.start_y) - self.start.height // 2
        self.end.x = relative_display_functions.get_relative_graph_x(self.end_x) - self.end.width // 2
        self.end.y = relative_display_functions.get_relative_graph_y(self.end_y) - self.end.height // 2

    def draw_new_path_lines(self):
        for line in self.path_lines:
            line.delete()
        self.path_lines.clear()
        if 0 <= global_game_data.current_player_index < len(config_data.player_data):
            # Set color for current player
            color = colors.GRAY[colors.SHAPE_INDEX]
            if 0 <= global_game_data.current_player_index < len(config_data.player_data):
                color = config_data.player_data[global_game_data.current_player_index][2][colors.SHAPE_INDEX]

            current_path = global_game_data.graph_paths[global_game_data.current_player_index]
            current_objective = global_game_data.player_objects[global_game_data.current_player_index].current_objective

            if 0 <= current_objective < len(current_path):
                # Draw line from player to next objective
                x_of_current_objective = relative_display_functions.get_relative_graph_x(
                    graph_data.graph_data[global_game_data.current_graph_index][current_path[current_objective]][0][0])
                y_of_current_objective = relative_display_functions.get_relative_graph_y(
                    graph_data.graph_data[global_game_data.current_graph_index][current_path[current_objective]][0][1])
                x_of_player = relative_display_functions.get_relative_graph_x(
                    global_game_data.player_objects[global_game_data.current_player_index].absolute_x)
                y_of_player = relative_display_functions.get_relative_graph_y(
                    global_game_data.player_objects[global_game_data.current_player_index].absolute_y)
                line_to_next_objective = pyglet.shapes.Line(
                    x_of_current_objective, y_of_current_objective, x_of_player, y_of_player,
                    color=color, thickness=3.0, batch=self.batch, group=self.group4)
                self.path_lines.append(line_to_next_objective)

                if current_objective < (len(current_path) - 1):
                    # Draw other lines later in path that player will travel to later
                    for index in range(current_objective + 1, len(current_path)):
                        x_of_indexed_objective = relative_display_functions.get_relative_graph_x(
                            graph_data.graph_data[global_game_data.current_graph_index][current_path[index]][0][0])
                        y_of_indexed_objective = relative_display_functions.get_relative_graph_y(
                            graph_data.graph_data[global_game_data.current_graph_index][current_path[index]][0][1])
                        x_of_previous_objective = relative_display_functions.get_relative_graph_x(
                            graph_data.graph_data[global_game_data.current_graph_index][current_path[index - 1]][0][0])
                        y_of_previous_objective = relative_display_functions.get_relative_graph_y(
                            graph_data.graph_data[global_game_data.current_graph_index][current_path[index - 1]][0][1])
                        line_to_objective = pyglet.shapes.Line(x_of_indexed_objective, y_of_indexed_objective,
                                                               x_of_previous_objective, y_of_previous_objective,
                                                               color=color, thickness=3.0, batch=self.batch,
                                                               group=self.group4)
                        self.path_lines.append(line_to_objective)

    def update_graph(self):
        self.resize_graph()
        self.draw_new_path_lines()

    def __del__(self):
        for graph_line in self.graph_lines:
            graph_line.delete()

        for graph_point in self.graph_points:
            graph_point.delete()