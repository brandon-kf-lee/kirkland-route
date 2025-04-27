import requests

# Define the Costco API endpoint
url = "https://www.costco.com/AjaxWarehouseBrowseLookupView"

# Define query parameters (latitude and longitude here are examples)
params = {
    'numOfWarehouses': '50',
    'hasGas': 'true',
    'populateWarehouseDetails': 'true',
    'latitude': '33.6846',
    'longitude': '-117.8265',
    'countryCode': 'US',
}

# Define headers
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-NZ,en;q=0.9",
    "cache-control": "max-age=0",
    "dnt": "1",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "cookie": "JSESSIONID=0000Eqc_6aA3uSYN3tWjudImaCV:1g39q5ouj; WAREHOUSEDELIVERY_WHS=%7B%22distributionCenters%22%3A%5B%221250-3pl%22%2C%221321-wm%22%2C%221456-3pl%22%2C%22283-wm%22%2C%22561-wm%22%2C%22725-wm%22%2C%22731-wm%22%2C%22758-wm%22%2C%22759-wm%22%2C%22847_0-cor%22%2C%22847_0-cwt%22%2C%22847_0-edi%22%2C%22847_0-ehs%22%2C%22847_0-membership%22%2C%22847_0-mpt%22%2C%22847_0-spc%22%2C%22847_0-wm%22%2C%22847_1-cwt%22%2C%22847_1-edi%22%2C%22847_d-fis%22%2C%22847_lg_n1f-edi%22%2C%22847_NA-cor%22%2C%22847_NA-pharmacy%22%2C%22847_NA-wm%22%2C%22847_ss_u362-edi%22%2C%22847_wp_r458-edi%22%2C%22951-wm%22%2C%22952-wm%22%2C%229847-wcs%22%5D%2C%22groceryCenters%22%3A%5B%22115-bd%22%5D%2C%22pickUpCenters%22%3A%5B%5D%7D; WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=OBHHSxO8hX6KevOMzC4Wvy%2FDgOobxvaF8SnMI%2FnzlO8%3D%3B2025-04-26+18%3A23%3A12.779_1745716992775-339353_10301_-1002%2C-1%2CUSD%2CKu8vVXIgsnqeLZHU1O3i3ZXWZrKMqLHEfvKpZcy9KueZL%2F9lJhJq5ncUd8Xo8A2w5Lh9d8DO9R6mWRC5qwAyeg%3D%3D_10301; WC_AUTHENTICATION_-1002=-1002%2CtMlGzWl0cXkJgxNmSw2bN88J4PwPTaLQto2HrkgAI8Q%3D; WC_ACTIVEPOINTER=-1%2C10301; WC_USERACTIVITY_-1002=-1002%2C10301%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C2076934830%2Cr1NxCoDGsvHPbVelaZfWYXb1kWqQfkgBoPf04QUytNIuafvRHGZVUjRut9Dnjcvl%2BC5Eahrys9mZy0dieNwdXLVJvEWCj8qnxXHCp0yiGFhhUp3THBn14f%2B%2FWrLlWlEXaH1eTX%2FS2QnP5RIXMY9W7ZpE805736rG7czrIL8Gbqwvlu%2F8EBs%2FKoQQzWoI54ODT9lY4G%2Fdf%2BgvZQlilIPm81hESYK3SqAoTeCx5RwywbFVNL2%2BdGwx9cBNp8rDWCLn; WC_GENERIC_ACTIVITYDATA=[44807369396%3Atrue%3Afalse%3A0%3AHyAG0RV5n7Vg%2B66mzghZg4SLj6oZYHE%2BZ0Dg%2BqfwlkM%3D][com.ibm.commerce.context.entitlement.EntitlementContext|120577%253B120572%253B120591%253B120563%253B120565%253B120570%253B120571%253B120568%253B120569%253B120757%253B120754%253B120752%253B120758%253B120753%253B120756%253B120755%253B120751%253B120765%253B120926%253B120762%253B120763%253B120761%253B120933%253B120920%253B120573%253B120574%253B4000000000000101005%253B60501%253B4000000000000001002%26null%26null%26-2000%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|1745716992775-339353][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.ExternalCartContext|null][com.costco.commerce.member.context.ProfileApiTokenCustomContext|null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null][com.costco.pharmacy.commerce.common.context.PharmacyCustomContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10701%26null%26false%26false%26false][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10301%26-1002%26-1002%26-1]; client-zip-short=91101; C_LOC=CA; AKA_A2=A; BCO=pm2; akavpau_zezxapz5yf=1745717293~id=aabbe5801b5c83b051921900d438df5c; akaas_AS01=2147483647~rv=39~id=09a6b8c0480c837a4164a647946823c7; bm_ss=ab8e18ef4e; _abck=259D4B78D4FF8052C4DA54299D9538E0~-1~YAAQC3HKFyVpHG2WAQAAyV7XdA22y10+MWcsLu+OJox7JAkkTGgAp3RAM0OTbCmcq3k5FdabGBr4+4Wkn9HJKNJb0NiQ2h9ybLiQqVSK0jFppoESeDwUHqj/72YVDFY/u/cfoKtw2WxhO7o4wIIfBK/o6oeZSuxXB3Hsp1Ok2IdwPKG0yR5U+SntJKOr+7lQUJgLmc35eqq1+AIrlg0WTZH4a4OCq2vP9yL2NmrHjAXT8z2L5CIzlQf2TSYRlRwAsGeJRNo0mY1Ka/typnjqqqDgWayicYCWteL1PGgWEAkFtZ/BGAoz/rCuY3xrPZxWtjSwTmtNAhThas7ezqaYnuVGRIPaDWnKHh6HWi/bN2dDiJdSxTpN1EC8LXba1cKC2GQEwttCTaD1hXdVHPzhEh9NfgtTxeTGMJrZ/Po=~-1~-1~-1; bm_s=YAAQC3HKFydpHG2WAQAAyV7XdAPqV7vDO5vnKlDrVmuUeSJ8CUX3Iv1UiP5WVaK2jKH49q/PCGjwEPi5AsZkPlpNR7TJ2bgqQV1sSlKdMV2GpILa0bBg314Jqcuj2jEcFYhG4zgv7eHDYjO3dnesEsne9ZUKH4V2l6yeZzfP26NygmK49jV8ceNOW0u+3yD1yjPtzoWX9JK9NRvs/EwehI1QzSIfY8ou0JI2ioQR1uw4JE5IEQfagnvyHrbblQDiuvK17IHc0r93mQLIlZn22ah8Pv7ZaSIvFGFsuoHPd3+dDHIbouNTuL4aqLKXWFeZ6EZJw8HGCMD0hkJCyjEE+9bpDq84u1RTrugPnRksgPAhz5wUo7c430BQRXpTPxp+qHCu0jPdUEfy2pXKjK1a30lYBjya/CJAnDgOICdsAs5/WxlLPY+5Mnz5ypV3ccR9rVBFOetB8UiX; bm_so=D97D4EDA5EEB69D762FEFE713099962CB80243EDAA8F09D52B309D3E4CDCA203~YAAQC3HKFyhpHG2WAQAAyV7XdAPokas2thsHJhBnlmEd+2gea6T6Cr8LTD4a2QwRrO1gRPNgH6xn9kMxtXCwfPdlNWuGYe8Xg7k0MYtUQhaX41VMINTgEyy7UgvpFNupITRJAEI6jxDkA4rO0qdxVZdk6VM0WyWqsTkN+6DcstDohbkFgiUqH5iNXhJ9n2HkPWPOIygaeysicuzSbtysGV/2L6+w3HNItsVQ0cNGXcFA07yOr/baLl1qE9BVC6iUr/6jz2AkGiLWXAmsd/2xxR+w8nSZIedBf936WQQwE9ok/+OwpEhtYbZ1avH/bQsuA2U04nKenv1aGFKHSS5D4lT3WI6WcjMD90e+y4LvjAgNnUS8iJywwCTK+xoGfMIPYdNckmHbQcgo3W5YPiwaGmlpgjVmqdko3l3NELOL+V7MINlg+pSzx7UjWNNUQdSptp/C5Ttbz0cH+VbWnXiY; bm_sz=CF91A2596E7B0378AA454959A1EE72B9~YAAQC3HKFylpHG2WAQAAyV7XdBusl9h6BFNnftToXp0eST40/Uh36AWfe703sh56/Kfi2uNw/n+wNvpdC4I7Py9YkkMsPcbShp/Mdx16MkmQLY0Y0VQLKkHIZpot8bsauzkfu3ZzhV1MLbfoVwMFVWskD4ZRAanUZIHYaPTUVeTkWPj+IM9kwtErq4MUYHD7WOAWRkJXNG1y2AVmVEUuQfYHNrg11sitS5YG4t3I2CShrXNMNsK0uCW+Qb5QfVz7YKbx4Zprh89Yi9U9w3rGTiK51th+0S/XI5r0FFPvdp0or/bmTT47dDX1GWYcWenVUemHjx4Pvw8q9cHktQ4vG22ZzvdoHIXq5Yqu+wKtEGb3atrUIUKAV3nffZweQKFrFtdFItsfPrKZhdl9AQ==~3553584~3490097",  # <<< IMPORTANT
}

print("Making request...")

# Make the request
response = requests.get(url, headers=headers, params=params, timeout=15)

# Debug output
print("Status code:", response.status_code)
print(response.text[:500])  # Preview first 500 chars

# Optional: If status is 200, try to parse JSON
# if response.status_code == 200:
#     try:
#         data = response.json()
#         #print("Parsed JSON:", data)
#     except Exception as e:
#         print("Failed to parse JSON:", e)