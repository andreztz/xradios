# Introduction

This documentation explains how to use the application, including keyboard shortcuts and commands. The application allows you to browse, play, and manage radio stations, with features like bookmarks (a list of favorite stations) and a command line for advanced controls.

# Help Window

The help window displays a list of keyboard shortcuts and commands. To close the help window, press `Esc`.

---

# Keyboard Shortcuts

This section lists the keyboard shortcuts for navigating and controlling the application.

## Global Shortcuts

| Shortcut         | Description                              |
|------------------|------------------------------------------|
| `Ctrl + Up`      | Navigate to the previous item            |
| `Ctrl + Down`    | Navigate to the next item                |
| `Ctrl + q`       | Close the application                    |

## Command Line

| Shortcut         | Description                              |
|------------------|------------------------------------------|
| `:`              | Open the command line                    |
| `Esc`            | Close the command line                   |

## List View

| Shortcut         | Description                              |
|------------------|------------------------------------------|
| `Up`             | Navigate to the previous station         |
| `Down`           | Navigate to the next station             |
| `p` or `Enter`   | Play the selected station                |
| `a`              | Add the selected station to bookmarks    |
| `d`              | Remove the selected station from bookmarks |
| `b`              | View the list of bookmarked stations     |

---

# Commands

Use these commands in the command line (accessed by pressing `:`).

## Bookmark Commands

- `bookmarks save=<line-number>`: Saves the station at the specified `<line-number>` to bookmarks. For example, `bookmarks save=3` saves the third station in the list.
- `bookmarks remove=<line-number>`: Removes the station at the specified `<line-number>` from bookmarks. For example, `bookmarks remove=3`.
- `bookmarks`: Displays the list of bookmarked stations.

## Search Command

Use the `search` command to find stations based on specific criteria. The format is:

`search option=value1, option="value2", ...`

**Options**:
- `order`: Sort results (e.g., `votes` for popularity).
- `limit`: Maximum number of results (e.g., `1000`).
- `hide_broken`: Set to `true` to hide stations that are not working.
- `tag_list`: A list of tags or categories, separated by commas (e.g., `"rock,jazz,pop"`).

**Example**:

`search order=votes, limit=1000, hide_broken=true, tag_list="rock,jazz"`


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
