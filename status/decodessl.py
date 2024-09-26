from gradio_client import Client

data = '''
-----BEGIN CERTIFICATE-----
MIIEhzCCA2+gAwIBAgIQU0cFbXEflQ8OZCigs97geDANBgkqhkiG9w0BAQsFADA7
MQswCQYDVQQGEwJVUzEeMBwGA1UEChMVR29vZ2xlIFRydXN0IFNlcnZpY2VzMQww
CgYDVQQDEwNXUjEwHhcNMjQwOTI1MTIwMzU0WhcNMjQxMjI0MTIwMzUzWjAhMR8w
HQYDVQQDExZ0aGVuYXlhbmthc3R1cmkuZXUub3JnMFkwEwYHKoZIzj0CAQYIKoZI
zj0DAQcDQgAEDDwlSl/sWoE/m4Aq7BT6caLIr5cKYcG7IotKtxSkR5vAffl2ixJC
RoFocitH6OkPGjTqZhmR6Z824ZwNOTfx2aOCAmowggJmMA4GA1UdDwEB/wQEAwIH
gDATBgNVHSUEDDAKBggrBgEFBQcDATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBRU
W/gDM78xLOers89W+dS3jpjJUzAfBgNVHSMEGDAWgBRmaUnU3iqckQPPiQ4kuA4w
A26ILjBeBggrBgEFBQcBAQRSMFAwJwYIKwYBBQUHMAGGG2h0dHA6Ly9vLnBraS5n
b29nL3Mvd3IxL1UwYzAlBggrBgEFBQcwAoYZaHR0cDovL2kucGtpLmdvb2cvd3Ix
LmNydDA+BgNVHREENzA1ghZ0aGVuYXlhbmthc3R1cmkuZXUub3JnghtkYXNoLnRo
ZW5heWFua2FzdHVyaS5ldS5vcmcwEwYDVR0gBAwwCjAIBgZngQwBAgEwNgYDVR0f
BC8wLTAroCmgJ4YlaHR0cDovL2MucGtpLmdvb2cvd3IxL1BPRnF2TWVmNEVZLmNy
bDCCAQIGCisGAQQB1nkCBAIEgfMEgfAA7gB1AHb/iD8KtvuVUcJhzPWHujS0pM27
KdxoQgqf5mdMWjp0AAABkilH9i4AAAQDAEYwRAIgItlHhThfydKl/aiPhEWNM+Z9
9P6gSrwjfijCMkwugHoCIEZIhcTlY5y7WvlYvHXEKeFxhl/JvYHCwQunlG8jg2yA
AHUA2ra/az+1tiKfm8K7XGvocJFxbLtRhIU0vaQ9MEjX+6sAAAGSKUf2NQAABAMA
RjBEAiAesCMYWpkzlJlIdZKtc38L0UDbl3S9ooA8AG7nuquwKgIgBV+94kudtmeI
Hl3blywQwia18ifWMiipE6GqI7iOiVIwDQYJKoZIhvcNAQELBQADggEBAEejBSMS
fnouzY67lHGTFddX71hTjCYB8BwQyyhZffzxwJ7g3sgZrZoG3gmJRrZAmS4srl+N
w7MRTpa6BjorAh0AFJZZOLVMClc9WDxQEXg1RtG1NuUXsxb4hXjCBnLmlIYv+IWK
mn5se0sbImMyCVmidpJLKJ928JdU9R8iCUkvdc0tA/TX1nInwWj7RNs2LrIDVLjl
WcbmJ1NUoC3LiCSimwgYF+Egd2ZqCi4uhSWhN8IHvJGSbZySqs0rMKjpEgcd/C3y
jjKnDRoSnX2oduslVX94h0t7QNo0CSkrCAcvJO5ZJ1OvrLDWF79H8x+h1h4WEmlx
EtSGpNUV5ml9jE8=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFCzCCAvOgAwIBAgIQf9niwtIEigR0tieibQhopzANBgkqhkiG9w0BAQsFADBH
MQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExM
QzEUMBIGA1UEAxMLR1RTIFJvb3QgUjEwHhcNMjMxMjEzMDkwMDAwWhcNMjkwMjIw
MTQwMDAwWjA7MQswCQYDVQQGEwJVUzEeMBwGA1UEChMVR29vZ2xlIFRydXN0IFNl
cnZpY2VzMQwwCgYDVQQDEwNXUjEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQDPbjYWircr7kaYAx1TcA937qNLoHK+jyMtwkfGj1yN+T3mGo7uMyINyRFI
uLBizvRpDXICfd7VJg/DbpvPfg7XIM/GkDujggbaOp3/bFa/3OlhlEXkabxPD8kT
wK1hRHIggdAPK55oamJqj4oiV3lpK+IkM352YyxdvFFpfiMHsf92gfHuuFi1azUV
76HmSCg5lzHZBx+Vp56uz5i8no2KA+Gwl01Qb5NMSh/4233xkJkVf+OW7e4xgepy
PVId3yVkpQtwqp7oqLlHyKdaECVgb0Lh1z/njwzwwoNGMyDmS3cEdqFop10VGO/Y
KHc1rQ6tRuRibuKq+MzvN34PJrMHAgMBAAGjgf4wgfswDgYDVR0PAQH/BAQDAgGG
MB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAGAQH/
AgEAMB0GA1UdDgQWBBRmaUnU3iqckQPPiQ4kuA4wA26ILjAfBgNVHSMEGDAWgBTk
rysmcRorSCeFL1JmLO/wiRNxPjA0BggrBgEFBQcBAQQoMCYwJAYIKwYBBQUHMAKG
GGh0dHA6Ly9pLnBraS5nb29nL3IxLmNydDArBgNVHR8EJDAiMCCgHqAchhpodHRw
Oi8vYy5wa2kuZ29vZy9yL3IxLmNybDATBgNVHSAEDDAKMAgGBmeBDAECATANBgkq
hkiG9w0BAQsFAAOCAgEATuazCBEgkWAn+VGQTQIY7rjBidUihJfm1t/mTjo7KQR+
3iDx4o2L06oeF0Q3wpKYpQgI/TeMqUlYMWQmZbWPE0PX8pfsVAE5E5tVOjh34bNA
JwDPVnsZVJwzN3nw5BGQ7sxRspFzIcM/qbbTpNeXf9II4Wsk2+Tv6FSVFZUL3/0u
HradbruDWjRQ4IZ7mYqKiEqk08dpOZ+TmBzwykEGy1/IXberb6Ap1SSnn2+RI7t6
N/fqPCrwwFjp8kg1G6etRATGBaPYCx+GjJMFPX+k97Alvoj3/98SvqdegLPYEPjv
xUclHpiKLD63NMmVarVQddIL6kOvTe5k0pnxRnR+mndGHIQc77TLbcZFeja56Pyn
lSqmer578c7CBrPqo1BVmPyWUK+v6sGuzs7Mq7QQaxVs4710cI/MpPp1ovxMVt17
ENKxLk34LpEKAKVmqwnzbHHRjhXNeCC984XDOwLEp0K4MzHl8ZOWJQAakCdVlFC+
PyA3GP2JX/QLoqWNHGuN9c9vLObDhHVs/L+65De+OdnnjpFGI9xxtsNyRsyaHdFA
f5z7ulOoXDXkHCCej/Ehs5docReNt16W2xbH/EBuirJrOzFE2rtALxksl1TdEjOf
IKXOJfUqQeVI5+hA7V+n1+A/n7Npg0S+5ODytWh5XW54ccN1drJnMK54ttozh0c=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFYjCCBEqgAwIBAgIQd70NbNs2+RrqIQ/E8FjTDTANBgkqhkiG9w0BAQsFADBX
MQswCQYDVQQGEwJCRTEZMBcGA1UEChMQR2xvYmFsU2lnbiBudi1zYTEQMA4GA1UE
CxMHUm9vdCBDQTEbMBkGA1UEAxMSR2xvYmFsU2lnbiBSb290IENBMB4XDTIwMDYx
OTAwMDA0MloXDTI4MDEyODAwMDA0MlowRzELMAkGA1UEBhMCVVMxIjAgBgNVBAoT
GUdvb2dsZSBUcnVzdCBTZXJ2aWNlcyBMTEMxFDASBgNVBAMTC0dUUyBSb290IFIx
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAthECix7joXebO9y/lD63
ladAPKH9gvl9MgaCcfb2jH/76Nu8ai6Xl6OMS/kr9rH5zoQdsfnFl97vufKj6bwS
iV6nqlKr+CMny6SxnGPb15l+8Ape62im9MZaRw1NEDPjTrETo8gYbEvs/AmQ351k
KSUjB6G00j0uYODP0gmHu81I8E3CwnqIiru6z1kZ1q+PsAewnjHxgsHA3y6mbWwZ
DrXYfiYaRQM9sHmklCitD38m5agI/pboPGiUU+6DOogrFZYJsuB6jC511pzrp1Zk
j5ZPaK49l8KEj8C8QMALXL32h7M1bKwYUH+E4EzNktMg6TO8UpmvMrUpsyUqtEj5
cuHKZPfmghCN6J3Cioj6OGaK/GP5Afl4/Xtcd/p2h/rs37EOeZVXtL0m79YB0esW
CruOC7XFxYpVq9Os6pFLKcwZpDIlTirxZUTQAs6qzkm06p98g7BAe+dDq6dso499
iYH6TKX/1Y7DzkvgtdizjkXPdsDtQCv9Uw+wp9U7DbGKogPeMa3Md+pvez7W35Ei
Eua++tgy/BBjFFFy3l3WFpO9KWgz7zpm7AeKJt8T11dleCfeXkkUAKIAf5qoIbap
sZWwpbkNFhHax2xIPEDgfg1azVY80ZcFuctL7TlLnMQ/0lUTbiSw1nH69MG6zO0b
9f6BQdgAmD06yK56mDcYBZUCAwEAAaOCATgwggE0MA4GA1UdDwEB/wQEAwIBhjAP
BgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBTkrysmcRorSCeFL1JmLO/wiRNxPjAf
BgNVHSMEGDAWgBRge2YaRQ2XyolQL30EzTSo//z9SzBgBggrBgEFBQcBAQRUMFIw
JQYIKwYBBQUHMAGGGWh0dHA6Ly9vY3NwLnBraS5nb29nL2dzcjEwKQYIKwYBBQUH
MAKGHWh0dHA6Ly9wa2kuZ29vZy9nc3IxL2dzcjEuY3J0MDIGA1UdHwQrMCkwJ6Al
oCOGIWh0dHA6Ly9jcmwucGtpLmdvb2cvZ3NyMS9nc3IxLmNybDA7BgNVHSAENDAy
MAgGBmeBDAECATAIBgZngQwBAgIwDQYLKwYBBAHWeQIFAwIwDQYLKwYBBAHWeQIF
AwMwDQYJKoZIhvcNAQELBQADggEBADSkHrEoo9C0dhemMXoh6dFSPsjbdBZBiLg9
NR3t5P+T4Vxfq7vqfM/b5A3Ri1fyJm9bvhdGaJQ3b2t6yMAYN/olUazsaL+yyEn9
WprKASOshIArAoyZl+tJaox118fessmXn1hIVw41oeQa1v1vg4Fv74zPl6/AhSrw
9U5pCZEt4Wi4wStz6dTZ/CLANx8LZh1J7QJVj2fhMtfTJr9w4z30Z209fOU0iOMy
+qduBmpvvYuR7hZL6Dupszfnw0Skfths18dG9ZKb59UhvmaSGZRVbNQpsg3BZlvi
d0lIKO2d1xozclOzgjXPYovJJIultzkMu34qQb9Sz/yilrbCgj8=
-----END CERTIFICATE-----

'''

client = Client("raannakasturi/decode_ssl")
result = client.predict(
		cert=data,
		api_name="/decode"
)
print(result)