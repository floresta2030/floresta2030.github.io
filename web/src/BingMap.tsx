import * as React from "react";
import { loadBingApi, Microsoft } from "./BingMapLoader";
import axios from "axios";
import { debounceTime } from "rxjs/operators";
import { Subject } from "rxjs";

interface IMapProps {
  mapOptions?: any;
}

const key = "AlhCe8XWn9qAY3ohEYMFdMNBiyKoBvIAW1X8XSiIXaip2kWTWy6jdLma-eCWCVsO";

export default class BingMap extends React.Component<IMapProps, any> {
  private mapRef = React.createRef<HTMLDivElement>();
  private map: any;
  private areasEntities: any = {};
  private pinEntities: any = {};
  private mapChanged = new Subject();

  private infobox: any;

  public componentDidMount() {
    loadBingApi(key).then(async () => {
      const map = this.initMap();
      this.map = map;

      Microsoft.Maps.loadModule("Microsoft.Maps.GeoJson", () => {
        Microsoft.Maps.Events.addHandler(map, "click", this.highlight);
        Microsoft.Maps.Events.addHandler(map, "viewchangeend", () =>
          this.mapChanged.next(map)
        );
        this.updatePins();
        this.infobox = new Microsoft.Maps.Infobox(map.getCenter(), {
          visible: false,
        });
        this.infobox.setMap(map);
      });
    });
    this.mapChanged.pipe(debounceTime(500)).subscribe(this.updatePins);
  }

  private updatePins = async () => {
    const zoom = this.map.getZoom();
    for (const pins in this.pinEntities) {
      for (const pin of this.pinEntities[pins]) {
        this.map.entities.remove(pin);
      }
      delete this.pinEntities[pins];
    }
    if (zoom < 10) {
      for (const areas in this.areasEntities) {
        for (const area of this.areasEntities[areas]) {
          this.map.entities.remove(area);
        }
        delete this.areasEntities[areas];
      }
      this.areasEntities = {};
    }
    const resp = await axios.get(
      `https://rodvieirasilva.pythonanywhere.com/pins?zoom=${zoom}&bounds=${
      //`http://localhost:5000/pins?zoom=${zoom}&bounds=${
        this.map.getBounds().bounds
      }`
    );
    for (const pin of resp.data) {
      this.areasEntities[pin.name] = this.areasEntities[pin.name] || [];
      this.pinEntities[pin.name] = this.pinEntities[pin.name] || [];
      let green = false;
      for (const geo of pin.geos) {
        var pushPin = new Microsoft.Maps.Pushpin(
          new Microsoft.Maps.Location(geo.lat, geo.lng),
          {
            text: pin.text,
            color: pin.color,
          }
        );
        pushPin.pin = pin;
        this.pinEntities[pin.name].push(pushPin);
        this.map.entities.push(pushPin);
        Microsoft.Maps.Events.addHandler(pushPin, "click", this.pushpinClicked);
        console.log(zoom, resp.data.length);
        if (zoom >= 10 && resp.data.length < 6) {
          if (this.areasEntities[pin.name].length != pin.geos.length) {
            var shape = Microsoft.Maps.GeoJson.read(geo.json);
            this.areasEntities[pin.name].push(shape);
            this.map.entities.push(shape);
          }
        }
      }
    }
  };

  private pushpinClicked = (e: any) => {
    const pin = e.target.pin;
    if (pin) {
      this.infobox.setOptions({
        location: e.target.getLocation(),
        title: pin.title,
        description: pin.description,
        visible: true,
      });
    }
  };

  private highlight = async (params: any) => {
    //const result = await axios.get();
    //console.log(params);
    console.log(params, this.map.getBounds(), this.map.getZoom());
  };

  public render() {
    return <div ref={this.mapRef} className="map" />;
  }

  private initMap() {
    const brazilBox = Microsoft.Maps.LocationRect.fromLocations(
      new Microsoft.Maps.Location(6.067439945929365, -10.128615333183788),
      new Microsoft.Maps.Location(-32.86130440585188, -94.50361533318379)
    );
    return new Microsoft.Maps.Map(this.mapRef.current, {
      mapTypeId: Microsoft.Maps.MapTypeId.aerial,
      minZoom: 5,
      bounds: brazilBox,
      center: new Microsoft.Maps.Location(
        -13.257928544766926,
        -49.121355290840725
      ),
    });
  }
}
