Explain infrastructure components in AWS.
VPC – private isolated network
Subnets – logical subdivisions (public/private)
Route Table – defines traffic routing
Internet Gateway – enables internet access
NAT Gateway – outbound internet for private subnets
Security Groups – instance-level firewalls
NACLs – subnet-level firewalls
ELB (ALB/NLB/CLB) – load balancing
ASG (Auto Scaling Group) – scaling EC2 instances
AMI – machine image used to launch instances
EBS – block storage for EC2
S3 – object storage



	Q. In Terraform, what is the purpose of init, plan, and apply commands?
	
	Terraform init  The terraform init command initializes a Terraform working directory
	 
	Terraform validate :- check the configuration is valid or not
	 
	Terraform plan :- shows changes needed by current configuration
	
	Terraform apply :- check and update the infrastructure
	
	Terraform destroyed >>it is used to destroy terraform managed infra



 Terraform Core Commands
1. terraform init :-  set up project (providers, modules, backend).
	• Purpose: Initializes a working directory for Terraform.
	• What it does:
		○ Downloads the required provider plugins (e.g., AWS, Azure, GCP).
		○ Configures the backend (where Terraform state is stored, e.g., S3, local).
		○ Prepares the directory to run further Terraform commands.
	• Run this once per project or after adding/changing providers/modules.

2. terraform plan :- Preview changes
	• Purpose: Shows what Terraform will do before actually applying changes.
	• What it does:
		○ Compares the desired configuration (in .tf files) with the current Terraform state and the real infrastructure.
		○ Outputs an execution plan:
			§ Resources to add (+)
			§ Resources to change (~)
			§ Resources to destroy (-)
	• Safe to run anytime to preview changes.
	• Helps avoid accidental resource deletions/changes.
1.Read Configuration: It reads your Terraform configuration files to understand what resources you want to create, update, or delete.
2. Compare State: It compares the current state of your infrastructure (as stored in the state file) with the desired state defined in your configuration files.
3. Generate a Plan: It generates a detailed plan showing the changes that will be made. This includes creating, modifying, or destroying resources.


3. terraform apply
	• Purpose: Executes the plan and makes the changes in real infrastructure.
	• What it does:
		○ Applies the execution plan to create/update/destroy resources.
		○ By default, asks for confirmation before applying (yes).
		○ Updates the Terraform state file after successful changes.

Q. What’s the difference between terraform apply, plan, and refresh?
Command	Purpose
terraform plan	Shows what changes Terraform will make (preview only).
terraform apply	Executes the plan and applies the changes to real infrastructure.
terraform refresh	Updates the local state file to match actual infrastructure without making changes.


1. Read Configuration: It reads your Terraform configuration files and the existing state file to understand the current infrastructure setup.
2. Create/Update/Delete Resources: Based on the configuration and the state file, it creates, updates, or deletes resources as necessary to achieve the desired state.
3. Show Execution Plan: Before making changes, terraform apply will show you the execution plan, detailing what actions will be taken.
4. Confirm Execution: It will prompt you to confirm that you want to proceed with the changes. You can type yes to confirm, or no to cancel.
To run terraform apply, navigate to your Terraform configuration directory in your terminal and execute:
 


 terraform validate:- check the configuration is valid or not

1. Syntax Checking: Verifies that your configuration files are correctly formatted and free of syntax errors.
2. Configuration Validation: Ensures that the configuration files are internally consistent and that all required variables and parameters are properly defined.

terraform validate
If there are any errors or issues with your configuration, Terraform will provide details on what needs to be fixed.


terraform init      # Setup providers and backend
terraform plan      # Preview changes
terraform apply     # Provision infrastructure

✅ Summary for interviews:
	• init → set up project (providers, modules, backend).
	• plan → preview execution changes.
	• apply → actually make changes and update state.


Q.What is the purpose of terraform validate and terraform fmt?
Command	Purpose	Example
terraform validate	Checks syntax and internal consistency of Terraform files (no changes applied).	terraform validate
terraform fmt	Formats Terraform code according to standard style (auto-fixes indentation and spacing).	terraform fmt
Usage flow:

terraform fmt       # Clean up code format
terraform validate  # Check correctness
terraform plan      # Preview infrastructure
terraform apply     # Deploy
Example:
	• If a variable is missing a closing brace → validate shows an error.
	• If code has inconsistent spaces → fmt corrects it automatically.


Q. What is a Terraform State File, and why is it essential/importantn?
	·  Basically json file(terraform.tfstate) ,that  stores information about the infrastructure Terraform manages.
	• Acts as a source of truth for Terraform.
	• Without it, Terraform doesn’t know which resources exist or need updates.
	• Needed for incremental changes, destroy operations, and dependency tracking.
	• Terraform maintains a state file (terraform.tfstate) that tracks all resources it manages — like EC2 instances, S3 buckets, IAM roles, etc
	• Enables Terraform to detect changes, plan updates, and avoid recreating existing resources.
	• Tracks real-world resources vs. the configuration in your .tf files.
	

	Q. Explain remote state locking in Terraform. 
	Terraform locks the state file using DynamoDB to prevent multiple users from modifying it at the same time. 

Q What is a Remote Backend in Terraform, and what are its advantages?
A Remote Backend stores Terraform state files in a remote location, such as:
		○ AWS S3
		○ Terraform Cloud
		○ Azure Storage, etc.


Q. How do you lock Terraform state to prevent conflicts?
	• When multiple people run Terraform simultaneously, it can corrupt the state file.
	• State locking prevents this by allowing only one operation at a time.
	• Example:
		○ When using S3 as a remote backend, enable DynamoDB table for state locking.
		○ Terraform will write a lock item to DynamoDB when applying changes and remove it after completion.
	• Command-level: locking happens automatically during plan or apply.


	Q. Managing Terraform State Securely in a Team
	• Use remote backends (instead of local terraform.tfstate) for collaboration:
		○ S3 + DynamoDB (AWS) → S3 stores state, DynamoDB locks it.
		○ Terraform Cloud / Enterprise
		○ Azure Storage Account / GCS bucket
	• Enable state locking to prevent concurrent writes.
	• Encrypt the state file at rest (S3 encryption or Terraform Cloud encryption).
	• Never commit state file to Git, because it can contain secrets like passwords or keys.

Advantages:
		• Collaboration: Shared state between team members.
		• State Locking: Prevents race conditions (e.g., via DynamoDB with S3).
		• Backups & Versioning: Automatically keep history of state changes.
		• Security: No sensitive data stored locally.
		Example configuration for S3 remote backend:
	
	
	terraform {
  backend "s3" {
    bucket = "my-tf-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "tf-locks"
  }
}
	
	
	
	 State Commands You Should Know
	Command	Description
	terraform state list	Lists all resources tracked in state
	terraform state show <resource>	Shows details of one tracked resource
	terraform state rm <resource>	Removes a resource from state (without deleting in cloud)
	terraform state mv <src> <dest>	Moves or renames resources inside the state
	terraform import <resource> <id>	Adds an existing real-world resource into state
	terraform refresh	Updates state with real infrastructure changes
	terraform output	Shows output values from the state file
	
	
Q, What happens if your state file is accidentally deleted?
	 Terraform loses track of managed infrastructure
	
Q. If a Terraform State File is deleted, how can you recover it?
If the state file is deleted, you lose Terraform's mapping to real resources, which can cause:
	• Re-creation of resources.
	• Inability to update or destroy existing infrastructure.

Recovery options:
	1. Remote Backend with versioning (e.g., S3):
		○ Roll back to an earlier version.
	2. Terraform Import:
		○ Rebuild the state by importing existing resources manually.
	3. Backup copy:
		○ Restore from a local or remote backup.

Q. How do you use remote backends (like S3 + DynamoDB) for storing Terraform state?
	• Remote backends allow shared, secure, versioned state storage.
	• Example:

terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
	• S3: stores state file
	• DynamoDB: provides state locking
	• Benefits:
		○ Collaboration (shared state)
		○ Versioning & backup
		○ Locking & consistency


Q.How does Terraform maintain the state of resources?
 What Is Terraform State?
Terraform maintains a state file (terraform.tfstate) that tracks all resources it manages — like EC2 instances, S3 buckets, IAM roles, etc.
It’s basically a snapshot of your real infrastructure at a point in time.

Where Is State Stored?
By default:
Terraform saves it locally in a file called terraform.tfstate in your working directory.
Example:

terraform.tfstate
It looks like JSON and contains details such as:

{
  "resources": [
    {
      "type": "aws_instance",
      "name": "myserver",
      "instances": [
        {
          "attributes": {
            "id": "i-0abc123def456",
            "ami": "ami-12345",
            "instance_type": "t2.micro"
          }
        }
      ]
    }
  ]
}


Q. How do you know your Terraform state and infrastructure are not in sync?
Terraform uses a state file to track what it created.
If something changes manually in the cloud, Terraform does not automatically know until you run:

terraform plan
This compares:
	• State file (what Terraform thinks exists)
	• Actual cloud resources (what really exists)
If they are different → Terraform shows changes, meaning state is not in sync.



✅ 3. How do you detect drift in Terraform?
Terraform Drift = when someone changes cloud resources manually (outside Terraform).
Ways to detect drift
	1. terraform plan → shows drift in output
	2. terraform refresh (older versions) → syncs remote state
	3. Terraform Cloud / Sentinel Policies
	4. Driftctl (open-source drift detection tool)
	5. Atlantis + GitOps workflows
Example: Load Balancer port changed from 443 → 80
If someone manually updates LB listener:
Run:

terraform plan
Terraform will show:

~ listener_port = 443 -> 80
This tells you exactly what drift happened.


✅ 5. What are Data Sources in Terraform?
Data sources allow Terraform to read or fetch existing information without creating resources.
Example:
	• Get latest AMI ID
	• Get existing VPC
	• Fetch existing IAM role
	• Lookup secrets from AWS Secrets Manager
Example:

data "aws_ami" "latest" {
  most_recent = true
  owners      = ["amazon"]
}



Q. What is Terraform Import, and why do we use it?
terraform import brings existing infrastructure under Terraform management without recreating it.
Use cases:
	• Legacy infrastructure created manually or by other tools.
	• Migrating existing cloud resources into Terraform’s control.
	• After a state file is lost or corrupted.
	Example:

	Q. Terraform import aws_instance.example i-0123456789abcdef0
This maps the EC2 instance to the Terraform resource in your .tf file.

	Q. How do you import existing resources into Terraform?
	• Used when infrastructure already exists and you want Terraform to manage it.
	• Command:

terraform import aws_instance.myserver i-0abcd1234ef567890
	• Then manually add the resource block in .tf file matching that resource type.
	• Note: It only adds the resource to the state, not automatically into the .tf files.



	Q. What is a Terraform module?
A Terraform module is a reusable set of configurations that can be used to create multiple resources with a consistent configuration.

	• A module is a reusable set of Terraform resources.
	• Can be thought of as a function in programming:
		○ Inputs → variables
		○ Logic → resources
		○ Outputs → outputs
Local vs Remote Modules
Type	Source	Use Case
Local Module	source = "./modules/vpc"	Reuse modules within the same repo/project
Remote Module	source = "git::https://github.com/user/repo.git" or Terraform Registry	Reuse modules from GitHub, GitLab, or Terraform Registry
Example of Local Module:

module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"
}
Example of Remote Module:

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"
  cidr    = "10.0.0.0/16"
}



Types of Modules
	1. Root Module
		○ The code in your main working directory (where you run terraform apply).
		○ Example: main.tf, variables.tf, etc.
	2. Child Module
		○ A reusable module, either:
			§ Local (from your file system)
			§ Remote (from Terraform Registry or GitHub)


resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
}
resource "aws_subnet" "my_subnet" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24"
}
You repeat this every time you need a new VPC.

 With a Module
Instead, use the official AWS VPC module:

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  azs             = ["us-east-1a", "us-east-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.101.0/24", "10.0.102.0/24"]
enable_nat_gateway = true
}
This single module block automatically creates:
	• VPC
	• Subnets
	• Internet gateway
	• NAT gateway
	• Route tables
	• Everything configured correctly 🎯


How It Works

module "name" {
  source = "where-to-get-it"
  # input variables
}
	• source → tells Terraform where the module code is (registry, git, or local folder).
	• Inputs (like name, cidr, etc.) are variables defined inside that module.
	• Terraform downloads the module, plugs in your inputs, and runs it as part of your plan.

📚 Common Sources
Source Type	Example
Terraform Registry	source = "terraform-aws-modules/vpc/aws"
GitHub	source = "github.com/user/repo//path/to/module"
Local Path	



 Q. How do you organize Terraform code for multiple environments (dev/stage/prod)?
Common approaches:
	1. Separate folders per environment:

├── environments/
    ├── dev/
    ├── stage/
    ├── prod/

Each has its own main.tf, variables.tf, and backend.tf.
	2. Use workspaces if environments share similar configurations but differ in variable values.
	3. Modules: Extract reusable logic (e.g., VPC, EC2) into modules, then call them with environment-specific variables.



Q. What happens internally when you run terraform apply?
	1. Loads configuration files (.tf).
	2. Initializes providers and modules.
	3. Refreshes state — compares actual resources with the state file.
	4. Generates execution plan.
	5. Applies changes using provider APIs (e.g., AWS, Azure).
	6. Updates the state file with new resource info.

 Q.  How do you handle secret variables in Terraform?
	• Do not store secrets directly in .tf files or .tfvars.
	• Use:
		○ Terraform Cloud/Enterprise — secure variable storage.
		○ Environment variables (export TF_VAR_db_password=...)
		○ Vault or AWS Secrets Manager integrations.
		○ Sensitive flag:

variable "db_password" {
  type      = string
  sensitive = true
}

→ hides value in logs and output.


	1. How do you provision infrastructure using terraform///.Workflow of core terraform
Steps to Provision Infrastructure with Terraform:
	1. Write Configuration Files (.tf):
		○ Define resources (EC2, S3, VPC, etc.) using HCL (HashiCorp Configuration Language).
		
	2. Initialize Terraform:

terraform init
	• Downloads providers and sets up the working directory.
	1. Plan the Deployment:

terraform plan
	• Shows what changes Terraform will make without applying them.
	1. Apply the Configuration:

terraform apply
	• Provisions the infrastructure on the cloud provider.
	1. Manage Changes:
		○ Update .tf files and re-run terraform plan → terraform apply to make changes.
	2. Destroy Infrastructure (Optional):

terraform destroy
	• Removes all resources defined in the configuration.





Terraform workspace
A Terraform workspace is basically Terraform’s built-in way of handling environment-specific state files — so yes, in many cases it’s used as an environment switch (dev, stage, prod, etc.) with the same Terraform code.

✅ Workspaces = Environment-specific Terraform
	• Each workspace = its own state file.
	• You can reuse the same configuration and deploy resources to multiple environments without copying code.
	• Example:

resource "aws_instance" "example" {
  ami           = "ami-123456"
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t2.micro"
  tags = {
    Name = "example-${terraform.workspace}"
  }
}
	• In dev workspace → creates a t2.micro
	• In prod workspace → creates a t3.large

 But, Some Important Nuances:
	• Workspaces are best when your environments are similar (just different sizes, tags, or counts).
	• For large/complex infra where environments diverge a lot, teams usually prefer separate folders/repos/backends(like environments/dev, environments/prod) instead of workspaces.
	• Workspaces = logical separation of state, not full isolation. (e.g., same S3 backend may still host multiple workspace states).

In short:
Yes — Terraform workspaces are mostly used as environment-specific Terraform states.
But they’re not the only way to manage environments; for complex infra, people often go for separate state files/backends instead of workspaces.





Terraform workspaces
 What are Terraform workspaces used for?
	• Workspaces allow multiple state files for the same configuration.
	• Common for separating dev, staging, prod within one codebase.
	• Commands:

terraform workspace new dev
terraform workspace select prod
	• Each workspace keeps its own state (e.g., terraform.tfstate.d/dev/terraform.tfstate).


A workspace in Terraform is an isolated environment that allows you to use the same Terraform configuration for multiple environments — like dev, staging, prod, etc. — each with its own state file.

environment-specific state files 


default   → local testing
dev       → developer environment
staging   → staging setup
prod      → production infrastructure


Without Workspaces	 With Workspaces
You must duplicate .tf files for each environment	 One .tf codebase, multiple environments
Harder to maintain consistency	 Easier to manage and promote changes
Single state file shared for all	Each workspace has its own state


Command	Description
terraform workspace list	Lists all workspaces
terraform workspace show	Shows the current active workspace
terraform workspace new <name>	Creates a new workspace
terraform workspace select <name>	Switches to an existing workspace
terraform workspace delete <name>	Deletes a workspace (must not be active)


terraform workspace new dev
terraform workspace select dev
terraform workspace list



Why We Use Terraform
1. Infrastructure as Code (IaC)
Terraform lets you define your infrastructure in code instead of clicking around in AWS, Azure, or GCP consoles.


1. How to manage diff envs using terraform?
By creating distinct terraform state files, making use of separate directories and variables for each env

2. What are Terraform modules and how do they help?
They are reusable components that improve the maintainability of Terraform code, enhance scalability in infrastructure as code projects by dividing up complex infrastructure into smaller parts.

4. What is Terraform's taint command used for?
When a resource instance is marked as tainted through the Terraform taint command, it must be destroyed and renewed on the next occasion to apply. It is used to trigger the recreation of a specific asset as a result of issues or configuration changes.

5. Can Terraform be utilized to manage infrastructure that is hosted on-premises?
Yes, Terraform can employ custom scripts or providers like VMware or OpenStack to manage on-premises infrastructure. It enables version control and automation via infrastructure as code practices


Q.How do you rollback infrastructure changes made with Terraform?
Core idea: Terraform doesn’t have an automatic “undo” button. You plan and apply deliberately.
Answer pattern:
	I handle rollbacks in Terraform by maintaining versioned state and Git-versioned IaC.
		○ First, I always run terraform plan and peer-review PRs before applying.
		○ State files are stored in remote backends (e.g., S3 + DynamoDB lock).
		○ If a change breaks something, I roll back by checking out the previous commit, re-running terraform apply, which reconciles the infra back to the previous configuration.
		○ For destructive changes, I test in a staging workspace first, and I often use Terraform workspaces to isolate environments.
		○ In some cases, I combine with infrastructure snapshots (e.g., AMI, RDS snapshot, S3 versioning) to restore data if necessary.
 Best practice keywords:
	• Git-driven IaC versioning
	• Remote backend (S3, DynamoDB lock)
	• Plan → Review → Apply
	• Rollback = re-apply previous version

 
 
Q.What is the purpose oth Hcl
describe infrastructure in a human-readable, declarative way — meaning you define what infrastructure you want, not how to create it.



Q.Default file created by tf to store exection plan?
terraform.tfplan
    - Keeps a snapshot of the proposed infrastructure changes.
    -Terraform generates a binary plan file called terraform.tfplan.


Q.terraform directory contain
The .terraform/ directory is a hidden working directory automatically created by Terraform in your project folder.
It stores metadata, provider plugins, modules, and state-related files that Terraform needs to manage your infrastructure.


Q.Which terraform file typically holds the resource configuration
>>main.tf

Q.How is iam used to in conjuction with terraform for aws
to provide credentials for accessing aws resources

Q.Terramform fmt? Function
Format .tf files in the current directory


What does --target option do when used with the terraform destroy command?




Q.write a simple terraform script to provision a virtual machine in aws

# ------------------------
# Provider
# ------------------------
provider "aws" {
  region = "us-east-1"  # Change as needed
}
# 
------------------------
# EC2 Instance
# ------------------------
resource "aws_instance" "my_ec2" {
  ami           = "ami-0c94855ba95c71c99"  # Replace with your AMI ID
  instance_type = "t2.micro"
  key_name      = "my-key"                 # Replace with your key pair name

tags = {
    Name = "MyTerraformVM"
  }
}
# ------------------------
# Output
# ------------------------
output "instance_public_ip" {
  value = aws_instance.my_ec2.public_ip
}

Steps to Use:
	1. Save as main.tf.
	2. Initialize Terraform:

terraform init
	3. Preview plan:

terraform plan
	4. Apply configuration:

terraform apply






 Q.How Terraform Maintains and Uses State
When you run Terraform commands:
1️⃣ terraform apply
	• Terraform compares your code (desired state) with the current state file (known state).
	• Then it queries the real infrastructure (actual state) from the cloud provider.
	• Based on the diff, it decides:
		○ What to create 🟢
		○ What to update 🟡
		○ What to destroy 🔴

2️⃣ terraform plan
	• Terraform reads the state file to know what exists.
	• It generates a plan showing changes needed to reach the desired configuration.

3️⃣ terraform refresh
	• Updates the state file with the latest info from real infrastructure — if something was changed manually in the cloud.

4️⃣ terraform destroy
	• Uses the state file to identify and destroy all resources Terraform created.

 Remote State (for Teams)
In team environments, local state isn’t safe — so we use remote state backends like:
Backend	Description
S3 + DynamoDB	Common for AWS, DynamoDB provides locking
Terraform Cloud	HashiCorp’s managed backend with versioning and access control
Azure Storage	For Azure teams
GCS (Google Cloud Storage)	For GCP users
Example: S3 backend configuration

terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
✅ This ensures:
	• Centralized state management
	• Locking (to prevent two people running Terraform at once)
	• Versioning (to recover old states)

⚡ Why State Is Important
Purpose	Description
Mapping real resources	Maps Terraform resources to cloud resources (e.g., EC2 instance ID)
Dependency tracking	Knows relationships between resources
Performance	Avoids querying cloud APIs every time
Drift detection	Detects manual changes outside Terraform
Safe updates/destroys	Ensures accurate lifecycle actions


🧾 Summary
Concept	Description
State File (terraform.tfstate)	Tracks infrastructure created by Terraform
Purpose	Map Terraform resources to real cloud resources
Default Location	Local directory
Recommended	Remote backend (S3, Terraform Cloud, etc.)
Used By	Plan, Apply, Destroy, Refresh





Q. Terraform Import vs Manually Defining Resources
Terraform Import
	• terraform import lets you bring existing infrastructure under Terraform management.
	• It does not generate .tf files automatically, only updates the state.
	• Example:

terraform import aws_instance.my_instance i-0123456789abcdef0
Manually Defining Resources
	• You write the .tf resource block yourself in code.
	• Terraform then creates/destroys it during apply.
	• Example:

resource "aws_instance" "my_instance" {
  ami           = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"
}
Key Difference
Aspect	Import	Manual
.tf Code	Not created automatically	You write it manually
State	Adds existing resource to state	State updated after apply
Use Case	Existing infra not managed by Terraform	New infrastructure managed from scratch



1. count
	• Purpose: Create multiple instances of a resource.
	• Example:

resource "aws_instance" "example" {
  count         = 3
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}

2. for_each
	• Purpose: Create multiple resources using a map or set.
	• Example:

resource "aws_s3_bucket" "buckets" {
  for_each = toset(["bucket1", "bucket2"])
  bucket   = each.value
  acl      = "private"
}

3. depends_on
	• Purpose: Explicitly declare dependencies between resources.
	• Example:

resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  depends_on    = [aws_vpc.main]
}

4. provider
	• Purpose: Specify which provider configuration to use for this resource.
	• Example:

resource "aws_instance" "example" {
  provider      = aws.secondary
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}

5. lifecycle
	• Purpose: Control resource lifecycle behavior (prevent destroy, ignore changes, create before destroy).
	• Example:

resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
lifecycle {
    prevent_destroy = true
    ignore_changes  = [acl]
    create_before_destroy = true
  }
}

6. timeouts
	• Purpose: Define custom create, update, or delete timeouts for a resource.
	• Example:

resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
timeouts {
    create = "30m"
    delete = "15m"
  }
}

7. dynamic (technically inside a block, not a resource argument)
	• Purpose: Dynamically generate nested blocks (not a top-level meta-argument, but often used with lifecycle, provisioners).
	• Example:

resource "aws_security_group" "example" {
  name = "example"
dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from
      to_port     = ingress.value.to
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr
    }
  }
}

8. provisioner
	• Purpose: Execute scripts or commands on the resource after creation or before destruction.
	• Example:

resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
provisioner "local-exec" {
    command = "echo Hello, World!"
  }
}

✅ Summary Table of Terraform Meta-Arguments
Meta-Argument	Purpose
count	Create multiple resource instances
for_each	Loop over map/set to create multiple instances
depends_on	Explicitly define resource dependencies
provider	Use a specific provider configuration
lifecycle	Control create/update/destroy behavior
timeouts	Set custom operation timeouts
provisioner	Run scripts/commands during resource lifecycle
dynamic	Dynamically generate nested blocks




2) How do you handle large-scale refactoring without downtime?
Answer: Use "terraform state mv" to rename resources without destroying them. Control changes with targeted applies. Split refactoring into multiple non-destructive PRs and verify plans carefully to prevent resource destruction.

3) What happens if a resource fails halfway through a terraform apply?
Answer: Terraform creates a partial deployment with successful resources running but failed ones marked as tainted. Use targeted applies and "-refresh-only" to recover systematically.


5) What happens if terraform plan shows no changes but infrastructure was modified outside Terraform?
Answer: Terraform remains unaware until "terraform refresh" is run. Implement regular drift detection in your CI/CD process to catch unauthorized changes.

6) What happens if you delete a resource definition from your configuration?
Answer: Terraform destroys the corresponding infrastructure. Either use "terraform state rm" first or implement "lifecycle {prevent_destroy = true }" for critical resources.

7) What happens if Terraform provider APIs change between versions?
Answer: Compatibility issues may arise. Always read release notes, use version constraints, test upgrades in lower environments, and consider targeted updates for gradual migration.

8) How do you implement zero-downtime infrastructure updates?
Answer: Use "create_before_destroy" lifecycle blocks, blue-green deployments, health checks, and state manipulation for complex scenarios. For databases, use replicas or managed services with failover capabilities.

9) What happens if you have circular dependencies in your Terraform modules?
Answer: Terraform fails with "dependency cycle" errors. Refactor module structure using data sources, outputs, or restructuring resources to establish clear dependency hierarchy.

10) What happens if you rename a resource in your Terraform code?
Answer: Terraform sees this as destroying and recreating the resource. Use "terraform state mv" to update state while preserving infrastructure, avoiding rebuilds and downtime.



3. How do you handle dependencies between resources in Terraform?
Terraform automatically handles dependencies based on the resource definitions in your configuration. It will create resources in the correct order.

4. What is Terraform's "apply" process?
The "apply" process in Terraform involves comparing the desired state from your configuration to the current state, generating an execution plan, and then applying the changes.

5. How can you manage versioning of Terraform configurations?
You can use version control systems like Git to track changes to your Terraform configurations. Additionally, Terraform Cloud and Enterprise offer versioning features.

6. What is the difference between Terraform and CloudFormation?
Terraform is a multi-cloud lac tool that supports various cloud providers, including AWS. CloudFormation is AWS-specific and focuses on AWS resource provisioning.


9. How does Terraform manage updates to existing resources?
Terraform applies updates by modifying existing resources rather than recreating them. This helps preserve data and configurations.

10. Can Terraform be used for managing third-party resources?
Yes, Terraform has the capability to manage resources beyond AWS. It supports multiple providers, making it versatile for managing various cloud and on-premises resources.

 
 
 Q.Can infrastructure be immutable and still be scalable?
Ans: Yes! That's the whole point. Tools like Terraform + image baking (e.g., Packer) allow infra to scale via prebuilt artifacts, not patching live systems.




	Q. How do you test your infrastructure code before deployment?
Answer approach: treat infrastructure as code → test like application code.
Example answer:
	I follow a layered testing strategy:
		○ terraform validate & terraform fmt to catch syntax and format issues early.
		○ terraform plan in CI to show a preview of proposed changes.
Bonus tip: mention using mock providers or sandbox AWS accounts for destructive-change testing.



	Q. How do you manage infrastructure using Terraform in Azure/AWS?
Terraform is an Infrastructure as Code (IaC) tool — it lets you define, provision, and manage cloud infrastructure using configuration files.
✅ Steps to manage infrastructure with Terraform:
	1. Install Terraform
Download and install from terraform.io.
	2. Set up Provider
		○ For AWS:

provider "aws" {
  region = "us-east-1"
}
		○ For Azure:

provider "azurerm" {
  features {}
}
	3. Write configuration files
Define resources such as EC2, S3, VPC (for AWS) or VM, Storage Account (for Azure).
Example (AWS EC2):

resource "aws_instance" "example" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
}
	4. Initialize Terraform

terraform init

→ Downloads provider plugins (AWS/Azure SDKs).
	5. Plan changes

terraform plan

→ Shows what will be created/modified/destroyed.
	6. Apply the configuration

terraform apply

→ Provisions real infrastructure.
	7. Destroy resources (when no longer needed)

terraform destroy
✅ In summary:
Terraform acts as a single tool to manage infrastructure lifecycle (create, update, delete) in both AWS and Azure, using declarative .tf files and version control.





Q. Explain how you set up an Auto Scaling Group in cloud using Terraform
An Auto Scaling Group (ASG) automatically adjusts the number of EC2 instances based on load.
Steps using Terraform (AWS example):

provider "aws" {
  region = "us-east-1"
}
# 1️⃣ Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "web-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "web-server"
    }
  }
}
# 2️⃣ Auto Scaling Group
resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 1
  vpc_zone_identifier  = ["subnet-xxxxxx"]   # Replace with your subnet ID
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
tag {
    key                 = "Name"
    value               = "web-asg-instance"
    propagate_at_launch = true
  }
}
✅ Explanation:
	• Launch Template → defines how EC2s are created (AMI, type, tags).
	• Auto Scaling Group → defines scaling rules (min, max, desired capacity).
	• Terraform manages the scaling infra so updates or deletions are controlled.
Commands:

terraform init
terraform plan
terraform apply




Q. What is taint and untaint in Terraform?
These commands are used when you need to force Terraform to recreate a specific resource.
terraform taint
Marks a resource as “tainted,” meaning Terraform will destroy and recreate it during the next apply.
Example:

terraform taint aws_instance.my_ec2
→ The next terraform apply will recreate that EC2 instance.
terraform untaint
Removes the tainted mark if you don’t want it to be recreated anymore.
Example:

terraform untaint aws_instance.my_ec2
✅ Use case:
If a resource becomes corrupted or misconfigured in real cloud infrastructure, instead of manually deleting it, you can taint it — Terraform ensures it’s rebuilt cleanly.



Q. How to manage sensitive variables in Terraform?
Sensitive variables (like passwords, keys, tokens) should never be hardcoded in .tf files.
✅ Best practices:
	1. Use terraform.tfvars or environment variables

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

Then define it in:

export TF_VAR_db_password="MySecret123"

or in terraform.tfvars (not checked into Git):

db_password = "MySecret123"
	2. Use .gitignore

*.tfvars
*.tfstate*

→ Prevents accidental commits of secrets.
	3. Use secret management systems
		○ AWS Secrets Manager
		○ Azure Key Vault
		○ HashiCorp Vault
		○ SOPS with Terraform Cloud
Example using AWS Secrets Manager:

data "aws_secretsmanager_secret_version" "db_secret" {
  secret_id = "db-password"
}

variable "db_password" {
  default = data.aws_secretsmanager_secret_version.db_secret.secret_string
}
	4. Mark variable as sensitive

variable "db_password" {
  sensitive = true
}

→ Terraform hides it in logs and plan output.








######



	Q. Create a VPC with Public & Private Subnet Launch two EC2 instances (one in public subnet, one in private subnet) Install Nginx on both instances using user_data.

Let’s build it step-by-step using Terraform — it will:
✅ Create a VPC
✅ Create Public & Private Subnets
✅ Create Internet Gateway (IGW)
✅ Create Route Tables
✅ Launch two EC2 instances (one in each subnet)
✅ Install Nginx on both using user_data

🧩 Terraform Script — main.tf

#######################################
# Provider
#######################################
provider "aws" {
  region = "us-east-1"
}
#######################################
# VPC
#######################################
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
tags = {
    Name = "MyDemoVPC"
  }
}
#######################################
# Internet Gateway
#######################################
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
tags = {
    Name = "MyDemoIGW"
  }
}
#######################################
# Public Subnet
#######################################
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
tags = {
    Name = "PublicSubnet"
  }
}
#######################################
# Private Subnet
#######################################
resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
tags = {
    Name = "PrivateSubnet"
  }
}
#######################################
# Public Route Table
#######################################
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.my_vpc.id
route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }
tags = {
    Name = "PublicRouteTable"
  }
}
#######################################
# Associate Public Subnet with Route Table
#######################################
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}
#######################################
# Security Group for EC2 Instances
#######################################
resource "aws_security_group" "web_sg" {
  vpc_id      = aws_vpc.my_vpc.id
  name        = "web_sg"
  description = "Allow HTTP and SSH"
ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
tags = {
    Name = "WebSecurityGroup"
  }
}
#######################################
# EC2 Instance in Public Subnet
#######################################
resource "aws_instance" "public_ec2" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_subnet.id
  key_name      = "my-keypair"             # Replace with your key pair
  vpc_security_group_ids = [aws_security_group.web_sg.id]
associate_public_ip_address = true
user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y nginx
              systemctl start nginx
              systemctl enable nginx
              echo "<h1>Hello from PUBLIC EC2 via Terraform!</h1>" > /usr/share/nginx/html/index.html
              EOF
tags = {
    Name = "PublicEC2"
  }
}
#######################################
# EC2 Instance in Private Subnet
#######################################
resource "aws_instance" "private_ec2" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.private_subnet.id
  key_name      = "my-keypair"
  vpc_security_group_ids = [aws_security_group.web_sg.id]
associate_public_ip_address = false
user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y nginx
              systemctl start nginx
              systemctl enable nginx
              echo "<h1>Hello from PRIVATE EC2 via Terraform!</h1>" > /usr/share/nginx/html/index.html
              EOF
tags = {
    Name = "PrivateEC2"
  }
}
#######################################
# Output the Public EC2 Public IP
#######################################
output "public_instance_ip" {
  value = aws_instance.public_ec2.public_ip
}



Q. Explanation of the Script
Section	Purpose
VPC	Creates an isolated network (10.0.0.0/16).
Subnets	Creates a public subnet (10.0.1.0/24) and private subnet (10.0.2.0/24).
Internet Gateway (IGW)	Enables internet access for public subnet.
Route Table + Association	Routes 0.0.0.0/0 traffic via IGW for the public subnet.
Security Group	Allows SSH (22) and HTTP (80).
Public EC2 Instance	Launches EC2 with a public IP and Nginx installed via user_data.
Private EC2 Instance	Launches EC2 without a public IP and installs Nginx internally.
Output	Prints the public IP of the public instance.

Q.Run Commands

terraform init
terraform plan
terraform apply -auto-approve
Then, copy the Public IP from the output:

http://<public_ip>
You should see:
	“Hello from PUBLIC EC2 via Terraform!”
The private instance will only be accessible from inside the VPC (e.g., SSH from the public EC2).





Q. Can you write a Terraform script for EC2 and S3?
	Here’s a simple Terraform script that creates:
		• an EC2 instance
		• an S3 bucket
	
	 main.tf
	
	# Specify the provider
provider "aws" {
  region = "us-east-1"
}
	# Create an S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-terraform-demo-bucket-12345"
  acl    = "private"
	tags = {
    Name        = "MyBucket"
    Environment = "Dev"
  }
}
	# Create a Security Group for EC2
resource "aws_security_group" "ec2_sg" {
  name        = "ec2_security_group"
  description = "Allow SSH and HTTP"
  vpc_id      = "vpc-xxxxxxx"  # Replace with your VPC ID
	ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
	ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
	egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
	tags = {
    Name = "EC2SecurityGroup"
  }
}
	# Create an EC2 Instance
resource "aws_instance" "my_ec2" {
  ami           = "ami-0c55b159cbfafe1f0"   # Example Amazon Linux 2 AMI (replace for your region)
  instance_type = "t2.micro"
  key_name      = "my-keypair"              # Replace with your keypair name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
	tags = {
    Name = "MyTerraformEC2"
  }
}
	


	A.  How do other teams use your Terraform modules & how do you version them?
	Best practice:
	📌 Store modules in a shared Git repo or Terraform Registry
	Teams reference via:
	
	module "vpc" {
  source  = "git::https://repo/vpc-module.git?ref=v1.2.0"
}
	✔ Semantic versioning → v1.0.0, v1.1.0
	✔ Tag releases → Teams don’t pick breaking changes accidentally
	✔ Document inputs/outputs → README.md
	Short answer:
		Shared Git/Registry modules with semantic versioning ensure reusability and controlled upgrades.


A. No downtime deployment when Terraform infra updates are needed
Use blue/green or rolling update strategy:
Resource type	Strategy
ASGs / Load-balancer backed apps	Create new infra → switch targets gradually
RDS/Databases	Multi-AZ failover
K8s nodes	Replace one by one (drain & cordon)
Networks	Parallel resources + phased migration
In Terraform:
	○ Enable create_before_destroy = true
	○ Use depends_on, lifecycle policies
	○ Apply changes during low-traffic windows
	○ Monitor via health checks
Short statement:
	Always create new infrastructure first and switch traffic gradually → zero downtime.


B. Introducing Terraform into an existing infrastructure
Approach: Import → Lock State → Manage Going Forward
Steps:
	a. Map existing infra → create Terraform code (IaC)
	b. Run:

terraform import <resource> <cloud-resource-id>
	c. Run terraform plan → fix config drift
	d. Store Terraform state in remote backend (S3 + DynamoDB lock)
	e. Enable pipeline (CI/CD) → Terraform becomes single control interface
Key message:
	Terraform should not recreate existing infra, only adopt it safely.


Q. Briefly explain the Terraform script you wrote
	Block	Purpose
	provider "aws"	Tells Terraform we’re using AWS as the cloud provider and sets the region.
	aws_s3_bucket	Creates an S3 bucket with private access and tags it.
	aws_security_group	Opens ports 22 (SSH) and 80 (HTTP) for the EC2 instance.
	aws_instance	Launches an EC2 instance using a specified AMI, type (t2.micro), and key pair. It also attaches the security group.

C. How do you connect Terraform with AWS?
Use AWS provider with credentials:
Option 1: Configure AWS CLI

aws configure
Terraform automatically picks credentials from:

~/.aws/credentials
Option 2: Environment variables

export AWS_ACCESS_KEY_ID="xxxx"
export AWS_SECRET_ACCESS_KEY="xxxx"
Provider config

provider "aws" {
  region = "ap-south-1"
}
Option 3: IRSA / IAM Roles (best for production)
• No static credentials
• Terraform assumes IAM role dynamically
Short answer:
Configure IAM credentials or assume role → Terraform AWS provider authenticates automatically.


D. Provision 100 EC2 instances & install application using CI/CD
Automation is the key:
1️⃣ Terraform → Provision EC2 at scale
2️⃣ UserData / Ansible / SSM → Install app automatically
3️⃣ Trigger via CI/CD pipeline (Jenkins/GitHub Actions):
• On commit → Terraform apply
• Post-deploy → configuration script executes
Better modern alternative:
Use Autoscaling Group + Launch Template to scale automatically.


Q. Using Terraform, create a complete infra (after sketching on whiteboard)
	Let’s create a sample AWS infrastructure with:
		• 1 EC2 instance
		• 1 S3 bucket
	Terraform Script: main.tf
	
	# ------------------------------
# Provider Configuration
# ------------------------------
provider "aws" {
  region = "us-east-1"
}
	# ------------------------------
# Create S3 Bucket
# ------------------------------
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-demo-bucket-terraform-example"
  acl    = "private"
	tags = {
    Name        = "MyS3Bucket"
    Environment = "Dev"
  }
}
	# ------------------------------
# Create EC2 Instance
# ------------------------------
resource "aws_instance" "my_ec2" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2 (example)
  instance_type = "t2.micro"
	tags = {
    Name = "MyEC2Instance"
  }
}






Q. How do you set up Kubernetes on AWS using EKS?
Here’s the step-by-step explanation 

Step 1: Create an EKS Cluster (using Terraform or AWS CLI)
You can create an EKS cluster in three main ways:
	1. AWS Management Console
	2. AWS CLI / eksctl (simplest method)
	3. Terraform (for IaC automation)

Using eksctl (recommended & simplest method):

# 1️⃣ Create EKS cluster
eksctl create cluster \
  --name my-eks-cluster \
  --region us-east-1 \
  --nodegroup-name my-eks-nodes \
  --node-type t3.medium \
  --nodes 2
# 2️⃣ Verify the cluster
kubectl get nodes
This command will:
	• Create an EKS control plane
	• Create worker nodes (EC2)
	• Configure kubectl automatically


✅ Using Terraform (more advanced & production-friendly):
	1. Use the official AWS EKS Terraform module:

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-eks-cluster"
  cluster_version = "1.29"
  subnet_ids      = ["subnet-xxxxx", "subnet-yyyyy"]
  vpc_id          = "vpc-xxxxxxx"

node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_types   = ["t3.medium"]
    }
  }
}
	2. Then run:

terraform init
terraform plan
terraform apply
	3. Configure your local system:

aws eks --region us-east-1 update-kubeconfig --name my-eks-cluster
kubectl get nodes

🧠 What’s happening behind the scenes:
	• Control Plane (managed by AWS) → Handles Kubernetes master components.
	• Worker Nodes (EC2) → Run your Pods and workloads.
	• Node Group → Autoscaling EC2 instances that act as workers.
	• kubectl → CLI to manage cluster resources.

✅ In Summary:
Task	Tool	Description
Create EKS Cluster	eksctl / Terraform	Sets up the managed K8s cluster
Configure access	aws eks update-kubeconfig	Adds kubeconfig entry
Verify setup	kubectl get nodes	Confirms worker nodes are active


++++


🎯 Short Interview Answer
“If the Terraform state file is deleted, Terraform loses track of your infrastructure and will try to recreate everything. You should always store state in a remote backend (S3, Terraform Cloud, etc.) to prevent loss. If state is deleted, recover it from backend versioning or use terraform import to rebuild the state manually.”





Q. I have to create 10 identical EC2 instances using Terraform — which approach do you use?
Two good approaches:
A. count or for_each on aws_instance — simple and direct:

variable "instance_count" { default = 10 }
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = "ami-xxxxxx"
  instance_type = "t3.micro"
  subnet_id     = var.subnet_id
  tags = {
    Name = "web-${count.index + 1}"
  }
}
B. (Recommended for production) Launch Template + Auto Scaling Group (ASG) — better for identical instances, scaling, consistent config, lifecycle management:

resource "aws_launch_template" "web" {
  name_prefix   = "web-"
  image_id      = "ami-xxxxxx"
  instance_type = "t3.micro"
tag_specifications {
    resource_type = "instance"
    tags = { Name = "web" }
  }
}
resource "aws_autoscaling_group" "web" {
  desired_capacity = 10
  min_size         = 10
  max_size         = 10
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  vpc_zone_identifier = var.subnet_ids
}
Why ASG/launch template?
	• Easier to manage lifecycle, updates (use rolling updates), integrate with ALB target groups, autoscaling, health checks.



Q. You created 10 VPCs manually, now need to create one EC2 instance using Terraform — how will you pass VPC id into Terraform script?
Pass the VPC id as a variable to the Terraform module/script. Use a variable and optionally a data source to find subnets inside that VPC.
Example variables.tf:

variable "vpc_id" {
  type = string
}
Use it to look up subnets and create an instance:

data "aws_subnet_ids" "selected" {
  vpc_id = var.vpc_id
}
resource "aws_instance" "example" {
  ami           = "ami-xxxxxx"
  instance_type = "t3.micro"
  subnet_id     = data.aws_subnet_ids.selected.ids[0]
  tags = { Name = "example-instance" }
}
How to supply variable:
	• CLI: terraform apply -var="vpc_id=vpc-0abc1234"
	• terraform.tfvars file:

vpc_id = "vpc-0abc1234"
	• Environment var: TF_VAR_vpc_id=vpc-0abc1234 terraform apply
If you need a specific subnet, either accept subnet_id as variable or filter data "aws_subnets" by tags.

Q.You provisioned a VPC with Terraform, someone deleted it manually — now you run terraform apply. How will your pipeline behave?
What Terraform will do (typical behavior):
	1. terraform plan / refresh: Terraform will compare the state file with the real infra. Because the VPC is absent but still present in Terraform state, Terraform will show that the VPC resource is planned to be created (it will appear as + create). Dependent resources managed by Terraform that were also deleted will also be planned to be recreated.
	2. terraform apply: If you run apply, Terraform will create the missing VPC and any dependent resources according to the configuration and state. The pipeline will succeed creating resources, unless there are conflicts or constraints (e.g., quota limits, name conflicts, resources manually recreated with different IDs that cause mismatches).
	3. Potential problem cases:
		○ If someone manually recreated resources with different attributes and those resources occupy the same names or CIDR blocks, Terraform may fail when trying to create resources that conflict (e.g., duplicate subnets with the same CIDR if the manually re-created resources used the same CIDR but different IDs).
		○ If other systems depend on the VPC, you may inadvertently overwrite or recreate resources and cause connectivity issues.
		○ If the state file is out-of-date or was lost/corrupted, terraform apply behavior might differ (might attempt to create many resources unexpectedly).







Q.Terraform script to provision an ec2 instance with custom security group and user data script
Here’s a complete Terraform example to provision an EC2 instance with a custom security group and user data script:

# ------------------------
# Provider
# ------------------------
provider "aws" {
  region = "us-east-1"  # Change as needed
}
# ------------------------
# Security Group
# ------------------------
resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow HTTP and SSH access"
  vpc_id      = "vpc-xxxxxxxx"  # Replace with your VPC ID
ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
tags = {
    Name = "web_sg"
  }
}
# ------------------------
# EC2 Instance
# ------------------------
resource "aws_instance" "web" {
  ami           = "ami-0c94855ba95c71c99"  # Replace with your AMI ID
  instance_type = "t2.micro"
  key_name      = "my-key"                 # Replace with your key pair name
  security_groups = [aws_security_group.web_sg.name]
# User Data script (example: install Apache)
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "Hello from Terraform" > /var/www/html/index.html
              EOF
tags = {
    Name = "WebServer"
  }
}
# ------------------------
# Output
# ------------------------
output "instance_public_ip" {
  value = aws_instance.web.public_ip
}
✅ Usage:
	1. Save this as main.tf.
	2. Initialize Terraform:

terraform init
	3. Preview the plan:

terraform plan
	4. Apply the configuration:

terraform apply



Q.What challenges do you face when multiple people update the same Terraform code?
Common challenges:
	• State file conflicts
	• Terraform lock failure
	• Merge conflicts in code
	• Unreviewed changes breaking infra
	• Inconsistent variable updates
	• Drifts caused by manual changes

Q. How do you structure Terraform code for best practices?
Follow a standard structure:

/modules
   /vpc
   /ec2
   /eks
/env
   /prod
   /dev
   /stage
main.tf
variables.tf
outputs.tf
provider.tf
Best practices:
	• Use modules for reusability
	• Keep environments separate
	• Use remote backend (S3 + DynamoDB lock)
	• Use version pinning for providers
	• Run Terraform through CI/CD
	• Enforce PR reviews

✅ 28. What was the recent challenging situation you faced?
Example answer (customize):
	Recently, our production Kubernetes cluster had high pod restarts due to misconfigured readiness probes. I troubleshot logs, identified wrong thresholds, fixed the probes, and deployed a patch using a rolling update without downtime.

✅ 29. What initiatives have you taken proactively?
Examples:
	• Implemented Terraform module standardization to reduce infra deployment time
	• Set up monitoring dashboards + alerts to detect issues early
	• Implemented S3 versioning + lifecycle policies to avoid accidental deletions
	• Created CI/CD templates to increase developer productivity
	• Automated AMI Patching via SSM or EC2 Image Builder


Q.why did you choose terraform over boto3 for infrastructurer provisioning?

1. Terraform vs Boto3 – Core Difference
Aspect	Terraform	Boto3
Type	Infrastructure as Code (IaC) tool	AWS SDK for Python (programmatic API calls)
State Management	Maintains state files to track deployed resources	No native state tracking; you have to manage resource states manually
Declarative vs Imperative	Declarative – You describe what you want, Terraform figures out how	Imperative – You write Python scripts that explicitly define how to create/update resources
Multi-Cloud Support	Yes – AWS, Azure, GCP, and more	No – Only AWS services
Reusability	High – Modules and HCL allow structured, reusable code	Moderate – Functions and scripts can be reused but less standardized
Rollback & Drift Detection	Built-in – Terraform can detect drift and revert changes	Manual – You must code rollback logic yourself
Community & Ecosystem	Large modules ecosystem for AWS, networking, security, etc.	Smaller – Limited to Python scripts and libraries



2. Why Choose Terraform
	1. Declarative Approach
		○ You define desired state; Terraform calculates the steps to achieve it.
		○ Example: “I want an EC2 instance with this AMI and this security group.” Terraform figures out creation, dependencies, and order.
	2. State Management
		○ Keeps track of all deployed resources in a state file.
		○ Makes updates, deletions, and drift detection safe and predictable.
	3. Multi-Cloud & Provider Agnostic
		○ If your project grows to use Azure or GCP, the same Terraform workflow can manage resources across clouds.
	4. Modules & Reusability
		○ Can create reusable modules for common patterns (VPC, ECS cluster, Lambda functions, RDS, etc.).
		○ Promotes standardization across teams and projects.
	5. Collaboration
		○ Terraform supports remote state storage, locking, and CI/CD integration.
		○ Multiple team members can safely manage the same infrastructure.
	6. Plan & Apply Workflow
		○ terraform plan shows exact changes before applying.
		○ Prevents accidental deletion or misconfiguration of critical resources.

3. When You Might Use Boto3 Instead
	• Automating AWS resource interactions from Python scripts, e.g., dynamically creating temporary S3 buckets or invoking Lambdas.
	• Performing complex logic or orchestration that is harder to express declaratively.
	• Integrating AWS operations inside an application rather than provisioning infrastructure at scale.

✅ Summary
	• Terraform = Best for infrastructure provisioning and management (declarative, stateful, reusable, multi-cloud).
	• Boto3 = Best for automation and programmatic AWS operations within applications or scripts (imperative, AWS-only).
	In most DevOps setups, Terraform is preferred for provisioning because it reduces human error, enables collaboration, and provides a clear declarative infrastructure-as-code workflow.
