output "gcp_cluster_name" {
  value = "${google_bigtable_instance.instance.name}"
}