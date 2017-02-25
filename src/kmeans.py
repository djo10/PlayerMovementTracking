from __future__ import print_function
import numpy, random, copy


class Cluster(object):
    def __init__(self, center):
        self.center = center
        self.data = []  # podaci koji pripadaju ovom klasteru

    def recalculate_center(self):
        new_center = [0 for i in xrange(len(self.center))]
        for datum in self.data:
            for i in xrange(len(datum)):
                new_center[i] += datum[i]

        n = len(self.data)
        if n != 0:
            self.center = [x / n for x in new_center]


class KMeans(object):
    def __init__(self, n_clusters, max_iter):
        """
        :param n_clusters: broj grupa (klastera)
        :param max_iter: maksimalan broj iteracija algoritma
        :return: None
        """
        self.data = None
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.clusters = []

    def fit(self, data, normalize=False):
        self.data = data  # lista N-dimenzionalnih podataka
        if normalize:
            self.data = self.normalize_data(self.data)

        dimensions = len(self.data[0])
        for i in xrange(self.n_clusters):
            point = [random.random() for x in xrange(dimensions)]
            self.clusters.append(Cluster(point))

        iter_no = 0
        not_moves = False
        while iter_no <= self.max_iter and (not not_moves):
            # Ispraznimo podatke koji pripadaju klasteru
            for cluster in self.clusters:
                cluster.data = []

            for datum in self.data:
                # Nadjemo indeks klastera kom pripada tacka
                cluster_index = self.predict(datum)
                # Dodamo tu tacku u taj klaster da bismo mogli izracunati centar
                self.clusters[cluster_index].data.append(datum)

            # Preracunamo centar
            not_moves = True
            for cluster in self.clusters:
                old_center = copy.deepcopy(cluster.center)
                cluster.recalculate_center()

                not_moves = not_moves and (cluster.center == old_center)

            print("Iter no: " + str(iter_no))
            iter_no += 1


    def predict(self, datum):
        min_distance = None
        cluster_index = None
        for index in xrange(len(self.clusters)):
            distance = self.euclidean_distance(datum, self.clusters[index].center)
            if min_distance is None or distance < min_distance:
                cluster_index = index
                min_distance = distance

        return cluster_index

    def euclidean_distance(self, x, y):
        sq_sum = 0
        for xi, yi in zip(x, y):
            sq_sum += (yi - xi) ** 2

        return sq_sum ** 0.5

    # Normalizovanje podataka
    def normalize_data(self, data):
        # Broj kolona
        cols = len(data[0])

        for col in xrange(cols):
            column_data = []
            for row in data:
                column_data.append(float(row[col]))

            mean = numpy.mean(column_data)
            std = numpy.std(column_data)

            for row in data:
                row[col] = (float(row[col]) - mean) / std

        return data

    def sum_squared_error(self):
        sse = 0
        for cluster in self.clusters:
            for datum in cluster.data:
                sse += self.euclidean_distance(cluster.center, datum)

        return sse ** 2