# -*- coding: utf-8 -*-
"""
Created on November 2019
@author: Laurent L. Santos
"""

from plotter import Plotter


def main():
    plotter = Plotter()

    # ===================================================================
    class Geometry:

        def __init__(self, name):
            self.__name = name

        def get_name(self):
            return self.__name

    # ===================================================================
    class Point(Geometry):
        def __init__(self, name, x, y):
            super ( ).__init__ ( name )
            self.__x = x
            self.__y = y

        def get_x(self):
            return self.__x

        def get_y(self):
            return self.__y

        def get_pts(self):
            pass

    # ===================================================================
    class PointReader:
        def __init__(self, points):
            self.points = points
            for i in self.points:
                pid = str(i[0])
                px = i[1]
                py = i[2]
                Point(pid, px, py)

     # ===================================================================
    class Line(Geometry):

        def __init__(self, name, point_1, point_2):
            super().__init__(name)
            self.__point_1 = point_1
            self.__point_2 = point_2

    # ===================================================================
    class Polygon(Geometry):

        def __init__(self, name, points):
            super().__init__(name)
            self.__points = points

        def get_points(self):
            return self.__points

        def lines(self):
            res = []
            points = self.get_points()
            point_a = points[0]
            for point_b in points[1:]:
                res.append(Line(str(point_a.get_name()) + "-" + str(point_b.get_name()), point_a, point_b))
                point_a = point_b
            res.append(Line(str(point_a.get_name()) + "-" + str(points[0].get_name()), point_a, points[0]))
            return res

    # ===================================================================
    class Reader:
        id, x, y = [], [], []

        def __init__(self, orig, prefix):
            self.id = []
            self.x = []
            self.y = []
            self.file = orig
            with open ( orig, "r" ) as f:
                next ( f, None )
                self.points = [[float ( x ) for x in row.split ( ',' )] for row in f.read ( ).split ( "\n" ) if row]
            with open ( orig, "r" ) as f:
                next ( f, None )
                for col in f.readlines ( ):
                    q, w, e = col.strip ( ).split ( ',' )
                    self.id.append ( str ( prefix + str ( q ) ) )
                    self.x.append ( float ( w ) )
                    self.y.append ( float ( e ) )
            for in_list in self.points:
                a = int ( in_list[0] )
                in_list[0] = prefix + str ( a )

        def get_points(self):
            return self.points

        def get_x(self):
            return self.x

        def get_y(self):
            return self.y

        def ret_id(self):
            return self.id

        def ret_reader(self):
            return self.id, self.x, self.y, self.file, self.points

    # ===================================================================
    #create geometry

    print("read polygon.csv" )

    path_pol = str(input("Please paste the filepath the csv file containing the coordinates if the polygon:") + "\polygon.csv")
    lectura_1 = Reader(path_pol, "prefix")
    poly_id, poly_x, poly_y, poly_file, poly_points = lectura_1.ret_reader()

    min_pol_x, max_pol_x, min_pol_y, max_pol_y = min(poly_x ), max(poly_x ), min(poly_y ), max(poly_y )

    path_in = input("Please paste the filepath of the csv file containing the points for testing the script:") + "\input.csv"
    lectura_2 = Reader(path_in, "pt")
    pt_id, pt_x, pt_y, ptfile, ptpoints = lectura_2.ret_reader()
    # point_inp = lectura_2.get_pts()

    # ===================================================================
    class Mbr:
        nc_id = []
        nc_x = []
        nc_y = []
        outside_id = []
        outside_x = []
        outside_y = []

        def __init__(self, points, min_x, min_y, max_x, max_y):
            self.nc_id = []
            self.nc_x = []
            self.nc_y = []
            self.nc_points = []
            self.outside_id = []
            self.outside_x = []
            self.outside_y = []
            self.outside_points = []
            self.points = points
            for i in self.points:
                tid = i[0]
                tx = i[1]
                ty = i[2]
                if min_x <= tx <= max_x and min_y <= ty <= max_y:
                    self.nc_id.append ( tid )
                    self.nc_x.append ( tx )
                    self.nc_y.append ( ty )
                    self.nc_points.append ( [tid, tx, ty] )
                else:
                    self.outside_id.append ( tid )
                    self.outside_x.append ( tx )
                    self.outside_y.append ( ty )
                    self.outside_points.append ( [tid, tx, ty] )

        def get_mbr_plot(self):
            return self.nc_x, self.nc_y, self.nc_points, self.outside_x, self.outside_y, self.outside_points
    # ===================================================================

    plotter.add_polygon(poly_x, poly_y)
    # plotter.add_point(pt_x, pt_y)

    print("categorize points")

    mbr1 = Mbr(ptpoints, min_pol_x, min_pol_y, max_pol_x, max_pol_y )

    nc_x, nc_y, nc_points, outside_x, outside_y, outside_points = mbr1.get_mbr_plot()


    plotter.add_point(nc_x, nc_y,)
    plotter.add_point(outside_x, outside_y, "outside")
    plotter.show( )

    with open ("output.csv","w") as f:
        for i, n in zip (ptpoints, mbr1 ):
            line= f.writelines(i+","+"\n")




if __name__ == "__main__":
    main ( )

