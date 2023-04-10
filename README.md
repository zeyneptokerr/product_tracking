Hi,

The goal of this project is to follow the constantly changing product prices.
For this, created three endpoint. 

First endpoint: /create-product-tracking -> We add the product we want to follow to the database by sending a request to this API. 
Parameters to enter when requesting: WebSiteName: we enter the site name on which we want to follow the product (Trendyol or HepsiBurada). SearchedProduct: we enter the price of which product we want to track. TotalFollowUpDays: we enter how many days we want to follow this product.
This way the product is inserting to the product table.

Second endpoint: /update-product-follow-up-days -> If we want to change the tracking day of the product we want to follow, we send a request to this API end.
Parameters to enter when requesting: SearchedProduct: We enter the name of the product for which we want to change the number of tracking days. TotalFollowUpDaysRemaining: We enter the number of days we want to follow the price of the product.
In this way, the remaining follow-up days of the product are updating from the product table.

Third endpoint: /delete-product-tracking -> If we no longer want to track the price of a product, we send a request to this API.
Parameters to enter when requesting: SearchedProduct: We enter the name of the product whose price we do not want to track.
In this way, the remaining tracking days of the product are updating as 0 from the product table.


For run this project: 
You can use this file by going to this path "product_tracking\api\main_tracking\database\database.vuerd.json" For create the tables in the database. Or you execute run the following script in database.

CREATE TABLE product
(
  id                             bigint     NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  website_name                   text       NOT NULL,
  product_name                   text       NOT NULL,
  total_follow_up_days           integer    NOT NULL,
  total_follow_up_days_remaining integer    NOT NULL,
  created_date                   timestamp  NOT NULL,
  update_date                    timestamp ,
  PRIMARY KEY (id)
);

CREATE TABLE product_tracking
(
  id                       bigint    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  product_id               bigint    NOT NULL,
  product_link             text      NOT NULL,
  product_brand            text     ,
  product_price            integer   NOT NULL,
  total_number_of_stars    float4   ,
  total_number_of_comments integer  ,
  created_date             timestamp NOT NULL,
  PRIMARY KEY (id)
);

ALTER TABLE product_tracking
  ADD CONSTRAINT FK_product_TO_product_tracking
    FOREIGN KEY (product_id)
    REFERENCES product (id);


While under the api folder enter the terminal -> 
1. pip install -r .\requirement.txt (We install all the libraries used.)
2. python main.py

If you want, you can import the following postman collection (product_tracking.postman_collection.json).
We add the product whose price we want to track by sending a request to the 0.0.0.0:4545/create-product-tracking API.

We open another terminal and run the command "python -m main_tracking.main".
In this way, we get the prices of the products we want to track every hour. The link and price of the product are inserting in the product_tracking table every hour.