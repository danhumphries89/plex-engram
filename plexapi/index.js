const { stat } = require('fs');

const   axios = require('axios'),
        express = require('express'),
        multer  = require('multer'),
        jsdom = require('jsdom'),
        { JSDOM } = jsdom,
        { exec } = require('child_process'),
        _ = require('underscore')

const   app = express()
const   port = 4567

var upload = multer({ dest: '/tmp/' });

const engram_collection = {
    'encoded' : [],
    'encrypted' : [],
    'decoherent' : ['44100'],
    'legendary' : ['48000', '96000'],
    'exotic' : ['88200', '192000']
};

app.post('/', upload.single('thumb'), function(request, response, next) {

    const payload = JSON.parse(request.body.payload);
    const isAudio  = (payload.Metadata.type === 'track')
    // const currentlyPlaying = (payload.event === ('media.play') || (payload.event === 'media.resume'))

    // @TODO: need to introduce positive and negative events to determine what happens to the 
    // Engram while music on Plex is playing. At the moment functions are executing at the wrong times
    const states = {
        'positive': [ 'media.play', 'media.resume', 'media.scrobble' ],
        'negative': [ 'media.stop' ]
    }

    // Need to grab the account ID (which should be 1) and limit the application
    // to only be modified by the first user (which we're assuming James' account will be)
    // This might also be worth adding to an .env file
    console.log( payload.event )
    
    if( isAudio && _.contains(states['positive'], payload.event) ) {

        // Just testing that everything is working as expected
        // console.log( payload.event )
        // console.log( payload.Metadata.title )

        // this should be an .env Token rather than hard coded here
        // might also be worth trying to add this as part of the install process
        const Token = "gsJZhghqCksrXBNXjPac"
        const config = {
            headers: {
                'Accept': 'application/xml',
                'Content-Type': 'text/xml'
            }
        }

        // Get the Sample & BitRate of the currently playing track
        axios.get(`http://192.168.1.81:32400${payload.Metadata.key}?X-Plex-Token=${Token}`, config)
            .then(( xml_repsonse ) => {
                var xml_dom = new JSDOM(xml_repsonse.data.toString(), { contentType: "text/xml" })
                var stream_children = xml_dom.window.document.querySelector('Part').children

                for( i=0; i < stream_children.length; i++ ) {
                    if( stream_children.item( i ).hasAttribute('samplingRate')) {
                        var sample_rate = stream_children.item( i ).getAttribute( 'samplingRate' );

                        for( var key of Object.keys(engram_collection) ) {
                            if( _.contains( engram_collection[key], sample_rate ) ){
                                console.log( "Sample Rate:", sample_rate )

                                // Tell Python that we need it to decode the Engram that's been dropped
                                exec( `sudo python3 /home/pi/Engram/engram-test.py ${ key }` );
                            }
                        }
                    }
                }
            });
    }
    else {
        console.log( "Stopping the Engram decode" );
        exec( `sudo python3 /home/pi/Engram/engram-test.py encoded --stop` );
    }

    response.sendStatus(200)
})

app.get('/', (req, response) => {
    response.send( "Hello, I'm sitting listening to Music...");
});

app.listen(port, () => {
    console.log('Plex Engram : Server Started...');
    exec( `sudo python3 /home/pi/Engram/engram-test.py encoded` );
})