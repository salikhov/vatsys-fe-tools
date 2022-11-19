from bs4 import BeautifulSoup
from polycircles import polycircles
import simplekml

INPUT = "Radars.xml"
OUTPUT = "Radars.kml"

METERS_IN_NM = 1852

def convert():
  with open(INPUT, "r") as input_file:
    bs = BeautifulSoup(input_file.read(), "xml")
    radars = bs.find_all("Radar")
    kml = simplekml.Kml()
    for radar in radars:
      lat = float(radar.Lat.text)
      long = float(radar.Long.text)
      range = int(radar.get("MaxRange"))
      name = str(radar.get("Name"))
      if long > 170 or long < -170:
        continue
      generate_radar_circle(kml, name, lat, long, range)
    kml.save(OUTPUT)
    

def generate_radar_circle(kml: simplekml, name, lat, long, range):
  polycircle = polycircles.Polycircle(latitude = lat, longitude = long, radius = range * METERS_IN_NM, number_of_vertices=36)
  polygon = kml.newpolygon(name = name, outerboundaryis=polycircle.to_kml())
  polygon.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.green)

def main():
  convert()

if __name__ == "__main__":
  main()