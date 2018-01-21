import matplotlib.pyplot as plt
import matplotlib.animation as animation


class LiveGraph:
    def __init__(self):
        self.lenOfPattern = 200
        self.xValues = list(range(1, self.lenOfPattern, 1))
        self.yValues1 = None
        self.yValues2 = None
        self.yValues3 = None
        self.yValues4 = None
        self.future_close_point = None
        self.close_points = None
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_title('Live graph and predicted outcome')
        self.ax1.set_xlabel('Index of Pattern')
        self.ax1.set_ylabel('Percentage Difference from first point')
        self._title = "Default"

    def animate(self, i):
        self.ax1.clear()
        self.ax1.plot(self.xValues, self.yValues1, c='k')
        try:
            self.ax1.scatter(self.lenOfPattern + 1, self.future_close_point, c='r', s=20)
            self.ax1.plot(self.xValues, self.yValues2, c='g')
            self.ax1.plot(self.xValues, self.yValues3, c='c')
            self.ax1.plot(self.xValues, self.yValues4, c='m')
            self.ax1.plot(self.xValues, self.close_points, c='r')
        except:
            print("Not enough patterns")
        self.fig.suptitle("Close: {} Close+5: {}".format(self._title, self.future_close_point))

    def start(self, pattern1, pattern2=None, pattern3=None, pattern4=None, close_points=None, future_close_point=None,
              title_text="Default"):
        self._title = title_text
        self.yValues1 = pattern1[-len(self.xValues):]
        if pattern2 is not None:
            self.yValues2 = pattern2[-len(self.xValues):]
        if pattern3 is not None:
            self.yValues3 = pattern3[-len(self.xValues):]
        if close_points is not None:
            self.close_points = close_points[-len(self.xValues):]
        if future_close_point is not None:
            self.future_close_point = future_close_point
        if pattern4 is not None:
            self.yValues4 = pattern4[-len(self.xValues):]
        ani = animation.FuncAnimation(self.fig, self.animate, interval=10)
        plt.show()
