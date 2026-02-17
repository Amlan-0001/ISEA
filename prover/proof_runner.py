# import subprocess
# import json
# import os

# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# def run_command(command):
#     result = subprocess.run(
#         command,
#         shell=True,           # Important for Windows (so npx works)
#         capture_output=True,
#         text=True
#     )
#     return result


# # ==========================================================
# # AGE PROOF
# # ==========================================================

# def generate_age_proof(dob_year, current_year, min_age=18):

#     input_data = {
#         "dob_year": dob_year,
#         "current_year": current_year,
#         "min_age": min_age
#     }

#     input_path = os.path.join(BASE_DIR, "circuits", "temp_age_input.json")
#     proof_path = os.path.join(BASE_DIR, "proofs", "age_proof.json")
#     public_path = os.path.join(BASE_DIR, "proofs", "age_public.json")
#     wasm_path = os.path.join(BASE_DIR, "circuits", "build_age", "age_js", "age.wasm")
#     zkey_path = os.path.join(BASE_DIR, "age_final.zkey")

#     with open(input_path, "w") as f:
#         json.dump(input_data, f)

#     command = f'npx snarkjs groth16 fullprove "{input_path}" "{wasm_path}" "{zkey_path}" "{proof_path}" "{public_path}"'

#     result = run_command(command)

#     if result.returncode != 0:
#         print(result.stderr)
#         return {"status": "fail", "message": "User is under 18"}

#     return {"status": "success"}


# # ==========================================================
# # ADDRESS PROOF
# # ==========================================================

# def generate_address_proof(country_code, state_code,
#                            required_country, allowed_state1, allowed_state2):

#     input_data = {
#         "country_code": country_code,
#         "state_code": state_code,
#         "required_country": required_country,
#         "allowed_state1": allowed_state1,
#         "allowed_state2": allowed_state2
#     }

#     input_path = os.path.join(BASE_DIR, "circuits", "temp_address_input.json")
#     proof_path = os.path.join(BASE_DIR, "proofs", "address_proof.json")
#     public_path = os.path.join(BASE_DIR, "proofs", "address_public.json")
#     wasm_path = os.path.join(BASE_DIR, "circuits", "build_address", "address_js", "address.wasm")
#     zkey_path = os.path.join(BASE_DIR, "address_final.zkey")

#     with open(input_path, "w") as f:
#         json.dump(input_data, f)

#     command = f'npx snarkjs groth16 fullprove "{input_path}" "{wasm_path}" "{zkey_path}" "{proof_path}" "{public_path}"'

#     result = run_command(command)

#     if result.returncode != 0:
#         print(result.stderr)
#         return {"status": "fail", "message": "Address invalid"}

#     return {"status": "success"}


# # ==========================================================
# # COMBINED KYC PROOF
# # ==========================================================

# def generate_kyc_proof(dob_year, current_year, min_age,
#                        country_code, state_code,
#                        required_country, allowed_state1, allowed_state2):

#     input_data = {
#         "dob_year": dob_year,
#         "current_year": current_year,
#         "min_age": min_age,
#         "country_code": country_code,
#         "state_code": state_code,
#         "required_country": required_country,
#         "allowed_state1": allowed_state1,
#         "allowed_state2": allowed_state2
#     }

#     input_path = os.path.join(BASE_DIR, "circuits", "temp_kyc_input.json")
#     proof_path = os.path.join(BASE_DIR, "proofs", "kyc_proof.json")
#     public_path = os.path.join(BASE_DIR, "proofs", "kyc_public.json")
#     wasm_path = os.path.join(BASE_DIR, "circuits", "build", "kyc_js", "kyc.wasm")
#     zkey_path = os.path.join(BASE_DIR, "kyc_final.zkey")

#     with open(input_path, "w") as f:
#         json.dump(input_data, f)

#     command = f'npx snarkjs groth16 fullprove "{input_path}" "{wasm_path}" "{zkey_path}" "{proof_path}" "{public_path}"'

#     result = run_command(command)

#     if result.returncode != 0:
#         print(result.stderr)
#         return {"status": "fail", "message": "KYC invalid"}

#     return {"status": "success"}
import subprocess
import json
import os

# 🔹 NEW: Import signature verification
from prover.signature_verify import verify_aadhaar_signature   # <-- ADDED

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result


# ==========================================================
# AGE PROOF (NOW AUTOMATICALLY USES VERIFIED AADHAAR DATA)
# ==========================================================

def generate_age_proof(current_year, min_age=18):
    """
    🔹 MODIFIED:
    - Removed dob_year parameter
    - Now extracts DOB from verified Aadhaar
    """

    # 🔹 NEW: Verify Aadhaar first
    verification_result = verify_aadhaar_signature()

    if verification_result["status"] != "valid":
        return {"status": "fail", "message": "Invalid Aadhaar Signature"}

    aadhaar_data = verification_result["aadhaar_data"]

    # 🔹 NEW: Extract DOB automatically
    dob_year = aadhaar_data["dob_year"]

    input_data = {
        "dob_year": dob_year,
        "current_year": current_year,
        "min_age": min_age
    }

    input_path = os.path.join(BASE_DIR, "circuits", "temp_age_input.json")
    proof_path = os.path.join(BASE_DIR, "proofs", "age_proof.json")
    public_path = os.path.join(BASE_DIR, "proofs", "age_public.json")
    wasm_path = os.path.join(BASE_DIR, "circuits", "build_age", "age_js", "age.wasm")
    zkey_path = os.path.join(BASE_DIR, "age_final.zkey")

    with open(input_path, "w") as f:
        json.dump(input_data, f)

    command = f'npx snarkjs groth16 fullprove "{input_path}" "{wasm_path}" "{zkey_path}" "{proof_path}" "{public_path}"'

    result = run_command(command)

    if result.returncode != 0:
        print(result.stderr)
        return {"status": "fail", "message": "User is under 18"}

    return {"status": "success"}


# ==========================================================
# ADDRESS PROOF (NOW AUTOMATICALLY USES VERIFIED AADHAAR DATA)
# ==========================================================

def generate_address_proof(required_country, allowed_state1, allowed_state2):
    """
    🔹 MODIFIED:
    - Removed country_code & state_code parameters
    - Now extracts address from verified Aadhaar
    """

    # 🔹 NEW: Verify Aadhaar first
    verification_result = verify_aadhaar_signature()

    if verification_result["status"] != "valid":
        return {"status": "fail", "message": "Invalid Aadhaar Signature"}

    aadhaar_data = verification_result["aadhaar_data"]

    # 🔹 NEW: Extract address automatically
    country_code = aadhaar_data["country_code"]
    state_code = aadhaar_data["state_code"]

    input_data = {
        "country_code": country_code,
        "state_code": state_code,
        "required_country": required_country,
        "allowed_state1": allowed_state1,
        "allowed_state2": allowed_state2
    }

    input_path = os.path.join(BASE_DIR, "circuits", "temp_address_input.json")
    proof_path = os.path.join(BASE_DIR, "proofs", "address_proof.json")
    public_path = os.path.join(BASE_DIR, "proofs", "address_public.json")
    wasm_path = os.path.join(BASE_DIR, "circuits", "build_address", "address_js", "address.wasm")
    zkey_path = os.path.join(BASE_DIR, "address_final.zkey")

    with open(input_path, "w") as f:
        json.dump(input_data, f)

    command = f'npx snarkjs groth16 fullprove "{input_path}" "{wasm_path}" "{zkey_path}" "{proof_path}" "{public_path}"'

    result = run_command(command)

    if result.returncode != 0:
        print(result.stderr)
        return {"status": "fail", "message": "Address invalid"}

    return {"status": "success"}


# ==========================================================
# COMBINED KYC PROOF
# ==========================================================

def generate_kyc_proof(current_year, min_age,
                       required_country, allowed_state1, allowed_state2):
    """
    🔹 MODIFIED:
    - Removed manual DOB & address inputs
    - Entire data comes from verified Aadhaar
    """

    # 🔹 NEW: Verify Aadhaar first
    verification_result = verify_aadhaar_signature()

    if verification_result["status"] != "valid":
        return {"status": "fail", "message": "Invalid Aadhaar Signature"}

    aadhaar_data = verification_result["aadhaar_data"]

    # 🔹 NEW: Extract all attributes automatically
    dob_year = aadhaar_data["dob_year"]
    country_code = aadhaar_data["country_code"]
    state_code = aadhaar_data["state_code"]

    input_data = {
        "dob_year": dob_year,
        "current_year": current_year,
        "min_age": min_age,
        "country_code": country_code,
        "state_code": state_code,
        "required_country": required_country,
        "allowed_state1": allowed_state1,
        "allowed_state2": allowed_state2
    }

    input_path = os.path.join(BASE_DIR, "circuits", "temp_kyc_input.json")
    proof_path = os.path.join(BASE_DIR, "proofs", "kyc_proof.json")
    public_path = os.path.join(BASE_DIR, "proofs", "kyc_public.json")
    wasm_path = os.path.join(BASE_DIR, "circuits", "build", "kyc_js", "kyc.wasm")
    zkey_path = os.path.join(BASE_DIR, "kyc_final.zkey")

    with open(input_path, "w") as f:
        json.dump(input_data, f)

    command = f'npx snarkjs groth16 fullprove "{input_path}" "{wasm_path}" "{zkey_path}" "{proof_path}" "{public_path}"'

    result = run_command(command)

    if result.returncode != 0:
        print(result.stderr)
        return {"status": "fail", "message": "KYC invalid"}

    return {"status": "success"}
