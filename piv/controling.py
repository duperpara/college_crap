import matplotlib
matplotlib.use('TkAgg')
import scipy
import matplotlib.pyplot as plt


def run():
    kp = 0
    ki = 0

    x = scipy.signal.step(
        scipy.signal.lti([6.1 * kp, 6.1 * ki], [64.5, (6.1 * kp + 1), 6.1 * ki])
    )
    x = scipy.signal.step(
        scipy.signal.lti([6.1 * kp, 6.1 * ki], [64.5, (6.1 * kp + 1), 6.1 * ki])
    )
    plt.plot(*x)
    plt.grid()
    plt.show()
    print()


if __name__ == '__main__':
    run()
