CREATE DATABASE `db_inquest`;
USE `db_inquest`;

CREATE TABLE `tb_pessoas`
(
  `pessoas_id`			int NOT NULL AUTO_INCREMENT,
  `pessoas_nome`		varchar(35) NOT NULL,
  `pessoas_sobrenome`	varchar(35) NOT NULL,
  `pessoas_cpf`			varchar(11) NOT NULL,
  `pessoas_email`		varchar(64) NOT NULL,
  `pessoas_end_com`		varchar(45) DEFAULT NULL,
  `pessoas_end_res`		varchar(45) NOT NULL ,
  `pessoas_cidade`		varchar(20) NOT NULL,
  `pessoas_estado`		varchar(20) NOT NULL,
  `pessoas_pais`		varchar(20) NOT NULL,
  `pessoas_telefone`	varchar(11) NOT NULL,
  `pessoas_celular`		varchar(11) NOT NULL,
  PRIMARY KEY (`pessoas_id`)
);

CREATE TABLE `tb_empresas`
(
  `empresas_id`			int NOT NULL AUTO_INCREMENT,
  `empresas_razao`		varchar(35) NOT NULL,
  `empresas_fantasia`	varchar(35) NOT NULL,
  `empresas_cnpj`		varchar(14) NOT NULL,
  `empresas_email`		varchar(64) NOT NULL,
  `empresas_end_com`	varchar(45) DEFAULT NULL,
  `empresas_end_cobr`	varchar(45) NOT NULL ,
  `empresas_cidade`		varchar(20) NOT NULL,
  `empresas_estado`		varchar(20) NOT NULL,
  `empresas_pais`		varchar(20) NOT NULL,
  `empresas_telefone`	varchar(11) NOT NULL,
  `empresas_celular`	varchar(11) NOT NULL,
  PRIMARY KEY (`empresas_id`)
);

CREATE TABLE `tb_bens`
(
  `bens_id`			int NOT NULL AUTO_INCREMENT,
  `bens_descricao`	varchar(35) NOT NULL,
  `bens_situacao`	varchar(35) NOT NULL,
  PRIMARY KEY (`bens_id`)
);

CREATE TABLE `tb_patrimonio`
(
  `patr_id`			 int NOT NULL AUTO_INCREMENT,
  `patr_pessoas_id`  int DEFAULT NULL,
  `patr_empresas_id` int DEFAULT NULL,
  `patr_bens_id` 	 int NOT NULL,
  PRIMARY KEY (`patr_id`)
);

CREATE TABLE `tb_socios`
(
  `socios_id`		   int NOT NULL AUTO_INCREMENT,
  `socios_pessoas_id`  int NOT NULL,
  `socios_empresas_id` int NOT NULL,
  PRIMARY KEY (`socios_id`)
);
