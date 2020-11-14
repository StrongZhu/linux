* server as 'JSON' data source, in grafana
   * NOT 'SimpleJson' data source
   * provide system service status, start/stop cmd
   * so we can use it in grafana. e.g. start/stop/status/service.
* API
   * `/` : for 'Test Connection' in data source config page
   * `/search` : return available metrics, for 'select metric' dropdown box, in query page
      * request
         * `type = timeseries/table`
      * response
         * can either return an **array** or **arrar of map (include 'text'/'value')** ,
         * sugguest use **array**
         * if return map, the 'value' will be in query request
   * `/query` : for data result
      * `targets' is a list, typically there is only 1 elemet
      * `targets[0]['type']` : 'timeseries/table'
      * `targets[0]['target']` : 'select metric', just like 'table' in MySql
   * `/annotions` : for XXXXXXXXX
   * `/tag-keys` : for XXXXXXXXX
   * `/tag-values` : for XXXXXXXXX
   * 
* reference : <https://grafana.com/grafana/plugins/simpod-json-datasource>