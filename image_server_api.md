# image_server
Server for receiving and sending images for BME 547 Class Demonstration

## Server API

URL is `http://vcm-21170.vm.duke.edu`.  (Port is 80, so not needed in URL)

### POST `/add_image`
Add an image to the database and display on webpage

Requires the following dictionary as JSON string
```python
{"image": <base_64_string>, "net_id": <net_id>, "id_no", <int>}
```
  + `<base_64_string>` is a string containing an image encoded into base 64
  + `<net_id>` is a string containing your Duke Net ID
  + `<int>` is an integer and will be used to tag the image for further retrieval

Returns `string` with message about the outcome of the Post.

### GET `/get_image_ids/<net_id>`

Retrieves a list of image ids stored on the server for the given net ID.  This
can be used if you cannot remember the image IDs you have used.

Variable URL where:
* `<net_id>` is the Duke Net ID used to store images

Returns a `list` in json-encoding containing integers of the image ids.

### GET `/get_image/<net_id>/<id_no>`

Retrieves the stored image with a watermark added.

Variable URL where:
  + `<net_id>` is the Duke Net ID used to store the image as above
  + `<id_no>` is the integer used to tag the image as above

Returns `string` containing the image encoded as a base 64 string.