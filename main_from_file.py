# -*- coding: utf-8 -*-
"""
Created on November 2019
@author: Laurent L. Santos
"""

from plotter import Plotter

def main():
    plotter = Plotter()

    # ===================================================================
    # parent class
    class Geometry:

        def __init__(self, name):
            self.__name = name

        def get_name(self):
            return self.__name

    # ===================================================================
    # subclass
    # to apply to the test point and polygon
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
    # Designed to extract values from the input polygon and test points
    # Sorts through and appends the data appropriately
    class Reader:
        id, x, y = [], [], []

        def __init__(self, orig):
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
                    self.id.append ( float ( q) )
                    self.x.append ( float ( w ) )
                    self.y.append ( float ( e ) )
            for in_list in self.points:
                a = int ( in_list[0] )
                in_list[0] = str ( a )

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
    # create geometry
    # Request filepath, opens and reads the CSVs files (polygon and test points)
    print("read polygon.csv" )
    path_pol = str(input("Please paste the filepath the csv file containing the coordinates if the polygon:") + "\polygon.csv")
    lectura_1 = Reader(path_pol)
    poly_id, poly_x, poly_y, poly_file, poly_points = lectura_1.ret_reader()

    min_pol_x, max_pol_x, min_pol_y, max_pol_y = min(poly_x ), max(poly_x ), min(poly_y ), max(poly_y )

    path_in = input("Please paste the filepath of the csv file containing the points for testing the script:") + "\input.csv"
    lectura_2 = Reader(path_in)
    pt_id, pt_x, pt_y, ptfile, ptpoints = lectura_2.ret_reader()

    # ===================================================================
    # MBR code is applied to see if the x and y values of each objects fall
    # within the minimum/ maximim x and y values

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
                    self.nc_points.append ( ["inside", tid, tx, ty] )
                else:
                    self.outside_id.append ( tid )
                    self.outside_x.append ( tx )
                    self.outside_y.append ( ty )
                    self.outside_points.append ( ["outside", tid, tx, ty] )

        def get_mbr_plot(self):
            return self.nc_x, self.nc_y, self.nc_points, self.outside_x, self.outside_y, self.outside_points
    # ===================================================================

    # Plotter.add_point(pt_x, pt_y)
    plotter.add_polygon(poly_x, poly_y)

    # Present the results
    print("categorize points")
    mbr1 = Mbr(ptpoints, min_pol_x, min_pol_y, max_pol_x, max_pol_y )
    nc_x, nc_y, nc_points, outside_x, outside_y, outside_points = mbr1.get_mbr_plot()

    # Create a output file with the classification os each point
    def merge_list(list_inside, list_outside):
        output = []

    # Print the results of points and classification
    print ( outside_points )
    print (nc_points)
    final_list = (nc_points + outside_points)

    # Save results on the file "output.csv"
    with open ("output.csv","w") as ff:
        for i in zip (final_list):
            line = ff.writelines ( str(i) + "," + "\n" )
        ff.write('\n')

if __name__ == "__main__":
    main ( )

