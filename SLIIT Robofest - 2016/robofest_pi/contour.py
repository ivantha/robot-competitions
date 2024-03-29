import cv2
import common


class Arrow:
    def __init__(self, contour, pos):             # pos is the position of the required point (starting position)
        self.pos = pos

        self.i0x = contour[pos][0][0]
        self.i0y = contour[pos][0][1]
        self.i1x = contour[(pos + 1) % 6][0][0]
        self.i1y = contour[(pos + 1) % 6][0][1]
        self.i2x = contour[(pos + 2) % 6][0][0]
        self.i2y = contour[(pos + 2) % 6][0][1]
        self.i3x = contour[(pos + 3) % 6][0][0]
        self.i3y = contour[(pos + 3) % 6][0][1]

        if pos == 0:
            self.in2x = contour[5][0][0]
            self.in2y = contour[5][0][1]
        elif pos == 1:
            self.in2x = contour[6][0][0]
            self.in2y = contour[6][0][1]
        else:
            self.in2x = contour[pos - 2][0][0]
            self.in2y = contour[pos - 2][0][1]

        self.mid_x = (self.i1x + self.i2x) / 2
        self.mid_y = (self.i1y + self.i2y) / 2

    def is_valid_arrow(self):
        m1 = self.get_i0_to_i1_gradient()
        m2 = self.get_i2_to_i3_gradient()

        d1 = self.get_i0_to_i1_distance()
        d2 = self.get_i2_to_i3_distance()

        c1 = abs(m1 - m2) <= 0.5
        c2 = (m1 == float('Inf') or m1 == float('-Inf')) and (m2 == float('Inf') or m2 == float('-Inf'))
        c3 = abs(d1 - d2) <= 15
        return (c1 or c2) and c3

    def get_i0_to_i1_gradient(self):
        return common.get_gradient(self.i0x, self.i0y, self.i1x, self.i1y)

    def get_i2_to_i3_gradient(self):
        return common.get_gradient(self.i2x, self.i2y, self.i3x, self.i3y)

    def get_i0_to_i1_distance(self):
        return common.get_distance(self.i0x, self.i0y, self.i1x, self.i1y)

    def get_i2_to_i3_distance(self):
        return common.get_distance(self.i2x, self.i2y, self.i3x, self.i3y)

    def get_main_axis_gradient(self):
        return common.get_gradient(self.in2x, self.in2y, self.mid_x, self.mid_y)

    def get_main_axis_intercept(self):
        return common.div((self.in2y * self.mid_x - self.mid_y * self.in2x), float(self.mid_x - self.in2x))

    def draw_initial_point(self, frame, radius=4, color=(255, 255, 255), thickness=2):
        cv2.circle(frame, (self.i0x, self.i0y), radius, color, thickness)

    def draw_mid_base_point(self, frame, radius=4, color=(255, 255, 255), thickness=2):
        cv2.circle(frame, (self.mid_x, self.mid_y), radius, color, thickness)

    def draw_head_point(self, frame, radius=4, color=(255, 255, 255), thickness=2):
        cv2.circle(frame, (self.in2x, self.in2y), radius, color, thickness)

    def enable_lines(self, frame):
        # Mid line
        cv2.line(frame, (self.mid_x, self.mid_y), (self.in2x, self.in2y), (255, 255, 255), 2)

        # Side lines
        # cv2.line(frame, (self.i0x, self.i0y), (self.i1x, self.i1y), (255, 255, 255), 2)
        # cv2.line(frame, (self.i2x, self.i2y), (self.i3x, self.i3y), (255, 255, 255), 2)

    def enable_labels(self, frame):
        # cv2.putText(frame, str(self.pos - 2), (self.in2x + 10, self.in2y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
        #             (255, 255, 255))
        cv2.putText(frame, str(self.pos), (self.i0x + 10, self.i0y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        # cv2.putText(frame, str(self.pos + 1), (self.i1x + 10, self.i1y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
        #             (255, 255, 255))
        # cv2.putText(frame, str(self.pos + 2), (self.i2x + 10, self.i2y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
        #             (255, 255, 255))
        # cv2.putText(frame, str(self.pos + 3), (self.i3x + 10, self.i3y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
        #             (255, 255, 255))
        cv2.putText(frame, str('HEAD'), (self.in2x + 20, self.in2y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        cv2.putText(frame, str('BASE'), (self.mid_x + 20, self.mid_y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
