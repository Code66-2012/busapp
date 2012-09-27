<?php
    header("content-type: text/xml");
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
?>
<Response>
    <Gather timeout="10" action="/phone_gather.php" method="GET">
        <Say voice = "woman">
            Welcome to Albuquerque Where's My Bus. At this time you must know the I D number of your bus stop to use this service. Enter it at any time followed by pound. You can lookup stop I D numbers using google maps by clicking on a bus stop. For updates about our service follow us on Twitter or Facebook.
        </Say>
    </Gather>
    <Say voice = "woman">No Input Received. Goodbye!</Say>
</Response>