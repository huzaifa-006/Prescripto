resource "aws_vpc" "main" {
  cidr_block           = var.vps_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "prescripto-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name = "prescripto-public-subnet"
  }
}

resource "aws_internet_gateway" "idw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "prescripto-idw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.idw.id
  }

  tags = {
    Name = "prescripto-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}