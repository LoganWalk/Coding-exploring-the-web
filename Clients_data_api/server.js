
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

const PORT = 3000;

const scheduleFile =
    path.join(
        __dirname,
        'weekly_schedule.json'
    );


app.use(
    express.json()
);


app.use(
    express.static(__dirname)
);


/*
 * SAVE WEEKLY SCHEDULE
 */
app.post(
    '/api/calendar/save',
    (req, res) => {

        try {

            const schedule =
                req.body;


            fs.writeFileSync(
                scheduleFile,
                JSON.stringify(
                    schedule,
                    null,
                    4
                )
            );


            console.log(
                'Schedule saved.'
            );


            res.json({
                success: true,
                message:
                    'Schedule saved successfully.'
            });

        }

        catch (error) {

            console.error(
                'Could not save schedule:',
                error
            );


            res.status(500).json({
                success: false,
                message:
                    'Could not save schedule.'
            });

        }

    }
);


/*
 * START SERVER
 */
app.listen(
    PORT,
    () => {

        console.log(
            `Calendar server running at http://localhost:${PORT}`
        );

    }
);