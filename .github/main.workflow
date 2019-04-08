workflow "CI" {
  on = "push"
  resolves = [
    "Dockerfile lint"
  ]
}

action "Dockerfile lint" {
  uses = "docker://cdssnc/docker-lint"
  args = "--ignore DL3013"
}