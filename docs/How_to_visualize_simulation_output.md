# How to visualize BISTRO simulation output

----
## 1. Requirements
### Database requirements
The simulation results from BISTRO should be parsed and saved to MySQL database before visualization. To install MySQL database you can follow official [Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/) or [google](https://www.google.com/) search how to install mysql on the specific operating system you are using, result from google search is usually simpler because the official guide from MySQL handles too many different cases. 

If you want to share output results on other machines different from the one running the simulation, it's recommended to install the MySQL database on a server that provides access to everyone who wants to visualize these shared simulation outputs.

### Visualization requirements
Git clone [BISTRO\_Dashboard](https://github.com/bistro-its-berkeley/BISTRO_Dashboard) to the machine that needs to visualize the output data. This machine should have access to the local/cloud MySQL database described above. 



----
## 2. Setup access
Assume MySQL has been installed, and root access has been created. Use`$ mysql -u root -p` to login to database.

Create bistro database inside mysql and configure account access, here we only use `usr` and `pswd` as example. Please use a secure username and password by your choice.

- `mysql> CREATE DATABASE bistro;`
- `mysql> CREATE USER ‘usr’ IDENTIFIED BY ‘pswd’;`
- `mysql> GRANT ALL ON bistro.* TO ‘usr’`

Now that MySQL has been configured, replace the credentials in the `ini` files.

> To connect to existing database, fill in the blanks in `BISTRO-Starter-Kit/utilities/dashboard_profile.ini` and `BISTRO_Dashboard/dashboard_profile.ini` with the credentials (i.e. `usr` and `pswd`). If the database is not hosted on the local machine, also change DATABASE\_HOST value to the IPv4 address of the intended database server.

----
## 3. Usage
The following code will parse and store the simulation results to the database, you should change the `city`, `sample_size`, `iteration` according to your simulation: 

- `$ cd utilities`
- `python`
- `>>> from simulation_to_db import parse_and_store_data_to_db`
- `>>> city = 'sioux_faux'`
- `>>> sample_size = '15k'`
- `>>> iteration = 30`
- `>>> output_root = '../output'`
- `>>> input_root = '../submission-inputs'`
- `>>>fixed_data = '../fixed-data'`
- `>>> output_path = '../output/<the_simulation_you_choose>'`
- `>>> parse_and_store_data_to_db(output_path, fixed_data, city, sample_size, iteration)`

After the above steps, follow the instruction from [BISTRO\_Dashboard](https://github.com/bistro-its-berkeley/BISTRO_Dashboard) to start the visualization process

----
## changelog
* 30-March-2020 init doc