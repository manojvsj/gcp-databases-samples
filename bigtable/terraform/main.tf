provider "google" {
  project = "${var.project_id}"
  region  = "europe-west1"
  credentials = "${file("${var.service_account_key_path}")}"
}

resource "google_bigtable_instance" "instance" {
  name         = "tf-instance"
  cluster {
    cluster_id   = "tf-instance-cluster"
    zone         = "europe-west1-b"
    num_nodes    = 3
    storage_type = "HDD"
  }
}