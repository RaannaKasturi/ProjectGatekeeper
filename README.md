# Project Gatekeeper: All-in-One SSL Toolkit
Project Gatekeeper is a comprehensive SSL toolkit designed to simplify SSL certificate management and enhance web security. The project provides a user-friendly interface and automates key processes like certificate generation, renewal, and monitoring, making SSL management more accessible to both novice users and experienced administrators. By integrating essential tools and leveraging modern technologies, Project Gatekeeper ensures SSL certificates are up-to-date and properly configured, contributing to a safer online environment.

## Backend Status
![Workflow Status](https://github.com/myusername/myrepo/actions/workflows/main.yml/badge.svg?event=status&status=${{ env.WORKFLOW_STATUS }})

## Key Features
- Certificate Generation Tool: Easily create SSL certificates with customizable parameters, reducing complexity and saving time.
- Certificate Decoding Tool: Decode SSL certificates into a human-readable format for troubleshooting and verification.
- Certificate Matcher Tool: Compare SSL certificates to ensure they meet specific requirements.
- Order Management Tool: Simplifies the process of ordering SSL certificates from trusted Certificate Authorities (CAs).
- SSL Integrity Checker: Monitors SSL certificates and provides alerts for expired or soon-to-expire certificates.

## Future Enhancements
- [ ] Custom CSR Generation: Users will be able to generate their own Certificate Signing Requests (CSRs) with personalized details, increasing flexibility.
- [ ] CSR-Based Orders: The toolkit will support ordering SSL certificates using custom CSRs directly through the interface.
- [ ] Certificate Revocation: Introduce a feature to revoke compromised or obsolete certificates, enhancing security.

## Deployment
- Backend: Hosted on Hugging Face Spaces, supporting up to 15 simultaneous requests.
- Frontend: Deployed on Vercel, providing an accessible and responsive interface for managing SSL certificates.

## Documentation & Resources
- ACME Documentation: [RFC 8555](https://datatracker.ietf.org/doc/html/rfc8555)
- Website: [Project Gatekeeper](https://projectgatekeeper.vercel.app/)
- Backend Repository: [ProjectGatekeeper](https://github.com/raannakasturi/projectgatekeeper)
- Frontend Repository: [ProjectGatekeeper_Website](https://github.com/raannakasturi/projectgatekeeper_website)

## References
- Aas, J., Barnes, R., Case, B., Durumeric, Z., Eckersley, P., Flores-López, A., Halderman, J. A., Hoffman-Andrews, J., Kasten, J., Rescorla, E., Schoen, S., & Warren, B. (2019). Let’s Encrypt. CCS ’19: Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security. https://doi.org/10.1145/3319535.3363192
- ACME Client Implementations. (2024, July 2). https://letsencrypt.org/docs/client-options/
- Documentation. (n.d.). https://letsencrypt.org/docs/
- Garcia-Font, V., & Àngel, L. Z. (2024, June 1). Renovación automática de certificados digitales con Let’s Encrypt. http://hdl.handle.net/10609/151124
- Pöpper, C., & Batina, L. (2024). Applied Cryptography and Network Security: 22nd International Conference, ACNS 2024, Abu Dhabi, United Arab Emirates, March 5–8, 2024, Proceedings, Part II. Springer. RFC 8555: Automatic Certificate Management Environment (ACME). (n.d.). IETF Datatracker. https://datatracker.ietf.org/doc/html/rfc8555
- Shoemaker, R. (2020a, February 1). RFC 8737: Automated Certificate Management Environment (ACME) TLS Application-Layer Protocol Negotiation (ALPN) Challenge Extension. IETF Datatracker. https://datatracker.ietf.org/doc/html/rfc8737
- Shoemaker, R. (2020b, February 1). RFC 8738: Automated Certificate Management Environment (ACME) IP Identifier Validation Extension. IETF Datatracker. https://datatracker.ietf.org/doc/html/rfc8738
- Welcome to acme-python’s documentation! — acme-python 0 documentation. (n.d.). https://acme-python.readthedocs.io/en/latest/
- Welcome to the Certbot documentation! — Certbot 2.11.0 documentation. (n.d.). https://eff-certbot.readthedocs.io/en/stable/index.html
