import * as React from "react";
import { loadBingApi, Microsoft } from "./BingMapLoader";

interface IMapProps {
    mapOptions?: any;
}

const key="AlhCe8XWn9qAY3ohEYMFdMNBiyKoBvIAW1X8XSiIXaip2kWTWy6jdLma-eCWCVsO";

export default class BingMap extends React.Component<IMapProps, any> {
  private mapRef = React.createRef<HTMLDivElement>();

  public componentDidMount() {
    loadBingApi(key).then(() => {
      this.initMap();
    });
  }

  public render() {
    return <div ref={this.mapRef} className="map" />;
  }

  private initMap() {
    const map = new Microsoft.Maps.Map(this.mapRef.current);
    if (this.props.mapOptions) {
      map.setOptions(this.props.mapOptions);
    }
    return map;
  }
}
