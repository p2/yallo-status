Yallo Status Checker
====================

Logs in to Yallo's user portal and extracts the remaining minutes, text and megabytes from all active plan options.

Use like:

    yallo-status.herokuapp.com?u={phone-number}&p={SIM-PUK}

Returns JSON like:

    {
      "options": [
        {
          "remaining": "983 MB",
          "renew": null,
          "service": "surf 2000"
        },
        {
          "remaining": "0 MB, 185 Minuten",
          "renew": "08.02.2015",
          "service": "Flex"
        }
      ]
    }
