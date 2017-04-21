DROP PROCEDURE IF EXISTS `business_drop_down_list`;
DELIMITER $$
CREATE PROCEDURE `business_drop_down_list`(
IN business_type varchar(20)
)
BEGIN
	SET @type_id = (SELECT business_type.id from business_type where business_type.name = business_type);
    SELECT
		bp_basic.bp_id as id,
        bp_basic.bp_name as name,
        replace('flags/1x1/{code}.svg', '{code}', lower(bp_location.country)) as countryFlag,
        contact.full_name as contactPerson,
        country.name as country
		FROM bp_basic
        INNER JOIN bp_basic_bp_types as bp_type on bp_type.bpbasic_id = bp_basic.bp_id
		LEFT OUTER JOIN bp_location on (bp_basic.bp_id = bp_location.bp_id and bp_location.is_primary = True)
		LEFT OUTER JOIN cities_light_country as country on bp_location.country = country.code2
		LEFT OUTER JOIN bp_contact as contact on (contact.bp_id = bp_basic.bp_id  and contact.is_primary=True)
        WHERE bp_type.businesstype_id = @type_id;

end$$
DELIMITER ;