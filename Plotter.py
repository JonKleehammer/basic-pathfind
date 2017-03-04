from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# method 'plot' which is called from the pathfind simulation.
# takes a list of 3 part tuples holding the xyz values for each data point
def plot(data):
    print len(data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
        xs = [int(i[0]) for i in data]
        ys = [int(i[1]) for i in data]
        zs = [int(i[2]) for i in data]
        ax.scatter(xs, ys, zs, c=c, marker=m)

    ax.set_xlabel('Tiles Checked')
    ax.set_ylabel('Goal Distance')
    ax.set_zlabel('Tiles Stored')

    plt.show()