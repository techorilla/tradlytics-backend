DELIMITER $$
CREATE DEFINER=`doniGroup`@`localhost` PROCEDURE `manifest_item_list`(
IN start_date datetime,
IN end_date datetime
)
BEGIN
    SELECT
		manifest_item.id,
		date,
		manifest_item.product_id as productId,
		product.name as productName,
		buyer_id as buyerId,
		buyer.bp_name as buyerName,
		buyer_country.name as buyerCountry,
		buyer_contact.full_name as buyerPrimaryContact,
		replace('flags/1x1/{code}.svg', '{code}', lower(buyer_location.country))  as buyerCountryFlag,
		seller_id as sellerId,
		seller.bp_name as sellerName,
		seller_country.name as sellerCountry,
		seller_contact.full_name as sellerPrimaryContact,
		replace('flags/1x1/{code}.svg', '{code}', lower(seller_location.country))  as sellerCountryFlag,
		quantity as quantity,
		quantity_metric_id as quantityMetricId,
		price_metric.metric as quantityMetric,
		manifest_item.container_no as containerNo,
		DATEDIFF(CURDATE(), manifest_item.created_at) <= 1 AS deleteable
		FROM manifest_item
		INNER JOIN bp_basic as buyer on buyer.bp_id = manifest_item.buyer_id
		INNER JOIN bp_basic as seller on seller.bp_id = manifest_item.seller_id
		INNER JOIN product on product.id = manifest_item.product_id
		INNER JOIN price_metric on manifest_item.quantity_metric_id = price_metric.id
		LEFT OUTER JOIN bp_location as buyer_location on (buyer_location.bp_id = buyer.bp_id and buyer_location.is_primary = True)
		LEFT OUTER JOIN bp_location as seller_location on (seller_location.bp_id = seller.bp_id and seller_location.is_primary = True)
		LEFT OUTER JOIN cities_light_country as buyer_country on buyer_location.country = buyer_country.code2
		LEFT OUTER JOIN cities_light_country as seller_country on seller_location.country = seller_country.code2
		LEFT OUTER JOIN bp_contact as buyer_contact on (buyer_contact.bp_id = manifest_item.buyer_id  and buyer_contact.is_primary=True)
		LEFT OUTER JOIN bp_contact as seller_contact on (seller_contact.bp_id = manifest_item.seller_id  and seller_contact.is_primary=True)
		where manifest_item.date  between start_date and end_date
        order by date desc;
end$$
DELIMITER ;
