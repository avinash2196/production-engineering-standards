# Vault policy template for a microservice.
# Apply with:  vault policy write <service-name> vault-policy.hcl
#
# Replace <SERVICE_NAME> with the kebab-case service name.
# Replace <ENVIRONMENT> with dev | staging | prod.

# ─── Read-only access to this service's secrets ───────────────────────────────
# Secrets must be stored under:  secret/data/<environment>/<service-name>/<key>

path "secret/data/<ENVIRONMENT>/<SERVICE_NAME>/*" {
  capabilities = ["read"]
}

# Allow reading secret metadata (list of keys, version info).
path "secret/metadata/<ENVIRONMENT>/<SERVICE_NAME>/*" {
  capabilities = ["list", "read"]
}

# ─── Database dynamic credentials ─────────────────────────────────────────────
# Uncomment if using the Vault database secrets engine.
# path "database/creds/<SERVICE_NAME>-<ENVIRONMENT>" {
#   capabilities = ["read"]
# }

# ─── PKI / TLS certificate issuance ──────────────────────────────────────────
# Uncomment if using Vault PKI for mTLS certificates.
# path "pki/issue/<SERVICE_NAME>" {
#   capabilities = ["update"]
# }

# ─── Explicit deny — catch-all ────────────────────────────────────────────────
# Vault denies by default; this explicit deny is only needed if you have a
# broader wildcard policy that might grant access you want to revoke.
# path "secret/data/prod/*" {
#   capabilities = ["deny"]
# }

