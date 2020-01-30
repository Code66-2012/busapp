INSERT INTO `times_simple` SELECT t.`arrival_time`,t.`stop_id`,c.`monday`,c.`saturday`,c.`sunday`,r.`route_short_name` FROM `times` t, `trips` tr, `calendar` c, `routes` r WHERE t.trip_id = tr.trip_id AND tr.route_id = r.route_id AND c.service_id = tr.service_id ;

INSERT INTO `trip_map` SELECT t.`trip_id`, t.`arrival_time`,t.`stop_id`,s.`stop_code`,t.`stop_sequence`,t.`shape_dist_traveled`,c.`monday`,c.`saturday`,c.`sunday`,r.`route_short_name` FROM `times` t, `trips` tr, `calendar` c, `routes` r,`stops` s WHERE t.trip_id = tr.trip_id AND tr.route_id = r.route_id AND c.service_id = tr.service_id AND t.stop_id = s.stop_id;

UPDATE `trip_map` SET `arrival_time` = CONCAT('0',TRIM(`arrival_time`)) WHERE CHAR_LENGTH(TRIM(`arrival_time`)) = 7;

UPDATE `times` SET `arrival_time` = CONCAT('0',TRIM(`arrival_time`)) WHERE CHAR_LENGTH(TRIM(`arrival_time`)) = 7;

UPDATE `times_simple` SET `arrival_time` = CONCAT('0',TRIM(`arrival_time`)) WHERE CHAR_LENGTH(TRIM(`arrival_time`)) = 7;

INSERT INTO `stops_local`(`stop_lat`, `stop_code`, `stop_lon`, `stop_id`, `stop_name`) SELECT `stop_lat`, `stop_code`, `stop_lon`, `stop_id`, `stop_name` FROM `stops`;

UPDATE stops_local INNER JOIN code66.stops ON (code66.stops.stopID = stops_local.stop_code) SET stops_local.direction = code66.stops.serves;

INSERT INTO `route_stop_map`(`route`, `stop`, `stop_code`) SELECT DISTINCT t.`route`, t.`stop_id`, s.`stop_code` FROM `times_simple` t, `stops` s WHERE s.stop_id = t.stop_id;
