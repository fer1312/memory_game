provider "aws" {
    region = "us-east-2"
}

resource "aws_security_group" "memorama_sg" {
    name        = "memorama-sg"
    description = "Permitir acceso a la API Flask"

    ingress {
        from_port   = 5000
        to_port     = 5000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "memorama" {
    ami           = "ami-0f30a9c3a48f3fa79"
    instance_type = "t3.micro"
    key_name      = "memorama-key"          # Key pair en AWS
    vpc_security_group_ids = [aws_security_group.memorama_sg.id]

    tags = {
        Name = "MemoramaAPI"
    }
}

output "public_ip" {
    value = aws_instance.memorama.public_ip
}
