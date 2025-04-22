# Help

To close this window press `ESC`.

---

# Bindings

## Globals: 

- Press `Ctrl + Up` or `Ctrl + Down` to move the focus.
- To close this app press `Ctrl + q`.

## Command Line:

- Press `:` to show the command line.
- Press `Esc` to close the command line.

## List View:

- Press `UP` or `Down` to navigate between list items
- Press `Enter` to play selected station

---

# Commands

## Bookmarks:

`bookmarks save=<line-number>`

`bookmarks remove=<line-number>`

`bookmarks`

## Search command:

`search option=value1, option="value 2", ....`

**Example:**

`search order=votes, limit=1000, hidebroken=true, tag_list='tag1,tag2,tag3'`


| Name              | Value               | Default           | Description                                                                                                                          |
|-------------------|---------------------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| name              | STRING              | OPTIONAL          | Name of the station.                                                                                                                  |
| name_exact        | false               | true, false       | OPTIONAL. If true, only exact matches will be considered. Otherwise, all matches will be included.                                    |
| country           | STRING              | OPTIONAL          | Country of the station.                                                                                                               |
| country_exact     | false               | true, false       | OPTIONAL. If true, only exact matches will be considered. Otherwise, all matches will be included.                                    |
| country_code      | STRING              | OPTIONAL          | 2-digit country code of the station (see ISO 3166-1 alpha-2).                                                                          |
| state             | STRING              | OPTIONAL          | State of the station.                                                                                                                 |
| state_exact       | false               | true, false       | OPTIONAL. If true, only exact matches will be considered. Otherwise, all matches will be included.                                    |
| language          | STRING              | OPTIONAL          | Language of the station.                                                                                                              |
| language_exact    | false               | true, false       | OPTIONAL. If true, only exact matches will be considered. Otherwise, all matches will be included.                                    |
| tag               | STRING              | OPTIONAL          | A tag of the station.                                                                                                                 |
| tag_exact         | false               | true, false       | OPTIONAL. If true, only exact matches will be considered. Otherwise, all matches will be included.                                    |
| tag_list          | STRING, STRING, ... | OPTIONAL          | A comma-separated list of tags. It can also be an array of strings in JSON HTTP POST parameters. All tags in the list have to match. |
| codec             | STRING              | OPTIONAL          | Codec of the station.                                                                                                                 |
| bitrate_min       | 0                   | POSITIVE INTEGER  | OPTIONAL. Minimum bitrate (in kbps) for the station.                                                                                   |
| bitrate_max       | 1000000             | POSITIVE INTEGER  | OPTIONAL. Maximum bitrate (in kbps) for the station.                                                                                   |
| has_geo_info      | both                | not set, true, false | OPTIONAL. If not set, display all stations. true shows only stations with geo_info, false shows only stations without geo_info.   |
| has_extended_info | both                | not set, true, false | OPTIONAL. If not set, display all stations. true shows only stations with extended information, false shows only stations without extended information. |
| is_https          | both                | not set, true, false | OPTIONAL. If not set, display all stations. true shows only stations with HTTPS URL, false shows only stations that stream unencrypted with HTTP. |
| order             | name                | name, url, homepage, favicon, tags, country, state, language, votes, codec, bitrate, lastcheckok, lastchecktime, clicktimestamp, clickcount, clicktrend, changetimestamp, random | OPTIONAL. Name of the attribute the result list will be sorted by. |
| reverse           | false               | true, false       | OPTIONAL. Reverse the result list if set to true.                                                                                      |
| offset            | 0                   | POSITIVE INTEGER  | OPTIONAL. Starting value of the result list from the database. For example, if you want to do paging on the server side.             |
| limit             | 100000              | 0, 1, 2, ...      | OPTIONAL. Number of returned data rows (stations) starting with offset.                                                                |
| hide_broken       | false               | true, false       | OPTIONAL. Whether to list broken stations or not.                                                                                      |
