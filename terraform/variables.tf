variable "aws_region" {
  default = "ap-south-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "instance_name" {
  default = "prescripto-server"
}

variable "key_pair_name" {
  description = "Existing EC2 Key Pair"
}

variable "vps_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  default = "10.0.1.0/24"
}