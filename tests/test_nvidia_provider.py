import os

from orch_bench.nvidia_provider import NvidiaProvider


def test_nvidia_provider_defaults_to_hosted_nemotron():
    provider = NvidiaProvider(api_key="test-key")
    assert provider.base_url == "https://integrate.api.nvidia.com/v1"
    assert provider.model == "nvidia/nemotron-3.5-lightning-30b-a3b"


def test_nvidia_provider_requires_api_key():
    old = os.environ.pop("NVIDIA_API_KEY", None)
    try:
        try:
            NvidiaProvider()
        except ValueError as exc:
            assert "NVIDIA_API_KEY" in str(exc)
        else:
            raise AssertionError("missing NVIDIA_API_KEY should fail")
    finally:
        if old is not None:
            os.environ["NVIDIA_API_KEY"] = old
