from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker, MarkerMapLayer
import definicje as d  


class AddLocationForm(BoxLayout): #clasa root
    search_long = ObjectProperty()
    search_lat = ObjectProperty()
    my_map = ObjectProperty()
    dt: ObjectProperty()
    rw: ObjectProperty()
    sp: ObjectProperty()
    sz: ObjectProperty()
    spr: ObjectProperty()
    ct: ObjectProperty()
    wm: ObjectProperty()
    wma: ObjectProperty()
        
    def Dane(self):
        file = 'krk2.gpx'
        if file.endswith('.gpx'):
            lon, lat, el, dates = d.Wczytaj(file)
            lat = lat[::10]   #wybieramy co 10 znacznik 
            lon = lon[::10]
            self.draw_route(lat,lon)
            dystans, Vsr, dH, wejscia, zejscia, Hmax, Hmin, h, m, s = d.zmienne(lon, lat, el, dates)
            self.dt.text = str(int((dystans)/1000)) + "km"
            self.rw.text = str(int(dH))
            self.sp.text = str(int(wejscia))
            self.sz.text = str(int(zejscia)) 
            self.spr.text = str(int(Vsr)) + "m/s"
            self.ct.text = str(h) + ":" + str(m) + ":" + str(s)
            self.wma.text = str(int(Hmax)) + "m"
            self.wm.text = str(int(Hmin))+ "m"
                       
            
    def draw_route(self,lat,lon):
        data_lay = MarkerMapLayer()
        self.my_map.add_layer(data_lay) # my_map jest obiektem klasy MapView
        for point in zip(lat,lon):
            self.draw_marker(*point,layer = data_lay)
            
    def draw_marker(self, lat, lon, layer = None):
        markerSource = 'dot.png'
        if lat != None and lon != None:
            marker = MapMarker(lat = lat, lon = lon, source = markerSource)
            self.my_map.add_marker(marker, layer = layer)
    



class MapViewApp(App):
    def build(self):
        return AddLocationForm()


if __name__ == '__main__':
    MapViewApp().run()
    
    