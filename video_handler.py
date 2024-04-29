import os

import cv2

from Constants import *


class VideoHandler:
    def __init__(self):
        self.VIDEOS_DIR = os.path.join('.', 'videos')

        self.video_path = os.path.join(self.VIDEOS_DIR, 'v1_short.mp4')  # get the video from the folder
        self.video_path_out = '{}_out.mp4'.format(self.video_path)  # create ending name for output file

        self.cap = cv2.VideoCapture(self.video_path)  # input source for cv2 library
        self.ret, self.frame = self.cap.read()  # ret - boolean (next frame exist), frame - encoding of current frame
        self.H, self.W, _ = self.frame.shape  # height, width, _ (of the frame)
        # output frame after writing on it
        self.out = cv2.VideoWriter(self.video_path_out, cv2.VideoWriter_fourcc(*'mp4v'),
                                   int(self.cap.get(cv2.CAP_PROP_FPS)), (self.W, self.H))

    def get_ret(self):
        return self.ret


    def get_top_right_corner(self):
        return (self.W - 1, 0)

    def paint_two_sides(self, game):
        cv2.rectangle(self.frame, (int(game.table.left_table[0]), int(game.table.left_table[1])),
                      (int(game.table.left_table[2]), int(game.table.left_table[3])), Color.RED, 4)
        cv2.rectangle(self.frame, (int(game.table.right_table[0]), int(game.table.right_table[1])),
                      (int(game.table.right_table[2]), int(game.table.right_table[3])), Color.AQUA, 4)


    def paint_frame_counter(self):
        cv2.putText(
            self.frame,
            f"Frame number: {Constants.counterUntilFrame}",
            (10, 30),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            Color.BLUE,
            2
        )
        self.out.write(self.frame)


    def read_next_frame(self):
        # print(f"Elapsed time: {elapsed_time_ms} milliseconds")
        self.ret, self.frame = self.cap.read()

    def get_frame(self):
        return self.frame

    def get_ret(self):
        return self.ret

    def paint_ball_movement(self, game):
        tmp_positions = game.ball.get_positions()
        for i, pos in enumerate(tmp_positions):
            if pos.is_vertical():
                cv2.circle(self.frame, (pos.x, pos.y), 15, (0, 0, 255), cv2.FILLED)
            else:
                cv2.circle(self.frame, (pos.x, pos.y), 5, (0, 255, 0), cv2.FILLED)
                # draw line between each frame.
            if i != 0:
                cv2.line(self.frame, (pos.x, pos.y), (tmp_positions[i - 1].x, tmp_positions[i - 1].y), Color.BLACK,
                         2)
            # cv2.putText(self.frame,f"the speed is {game.ball.speed}", (pos.x+10, pos.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, Color.CYAN, 2)

    def paint_all(self, x1, y1, x2, y2):
        cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), Color.GREEN, 4)
    # cv2.putText(self.frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1.3, Constants.GREEN, 3, cv2.LINE_AA, )

#draw live result of the game
    def draw_result(self):
        top_right=self.get_top_right_corner()
        # Coordinates for the rectangle
        top_left_x = top_right[0]/2 - 250
        top_left_y = top_right[1]
        bottom_right_x = top_right[0]
        bottom_right_y = top_left_y + 250

        # Draw the rectangle
        cv2.rectangle(self.frame, (int(top_left_x), int(top_left_y)), (int(bottom_right_x), int(bottom_right_y)),
                      Color.BLACK, -1)  # -1 is for fill the rectangle
        cv2.putText(self.frame, f"Left {Constants.L_RESULT} - Right {Constants.R_RESULT}", (int(top_left_x) + 30, int(top_left_y) + 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, Color.AQUA, 5, cv2.LINE_AA, )

    def release(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
