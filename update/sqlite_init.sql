CREATE TABLE [version] (
[version] INTEGER  NOT NULL
);
INSERT INTO `version` VALUES ('3');
CREATE TABLE "android_metadata" ("locale" TEXT DEFAULT 'en_US');
INSERT INTO `android_metadata` VALUES ('en_US');
CREATE INDEX [IDX_STOPS_LAT] ON [stops_local](
[stop_lat]  ASC,
[stop_lon]  ASC
);
CREATE INDEX [IDX_ROUTES_STOP] ON [route_stop_map](
[stop_code]  ASC
);
