---
title: "Valkey for AI"
description: Repositories and frameworks that integrate with Valkey for AI workloads
---

# Valkey for AI

This page contains links to repositories that integrate with Valkey for AI workloads. It serves as a collection of resources for developers building AI applications.

## [LMCache](https://github.com/LMCache/LMCache)

KV cache management engine for LLM serving that reduces time-to-first-token and increases throughput. Valkey serves as a remote storage backend for KV cache reuse across vLLM and SGLang instances, allowing any serving engine to share cached prefill results.

- [Valkey backend documentation](https://docs.lmcache.ai/kv_cache/storage_backends/valkey.html)
- [Valkey connector source](https://github.com/LMCache/LMCache/blob/dev/lmcache/v1/storage_backend/connector/valkey_connector.py)
- [Valkey benchmarking example](https://github.com/LMCache/LMCache/tree/dev/examples/kv_cache_reuse/remote_backends/valkey)

## [Haystack](https://github.com/deepset-ai/haystack)

Framework for building search and RAG pipelines. Valkey serves as a ValkeyDocumentStore for storing documents with embeddings and running vector similarity search within Haystack pipelines.

- [valkey-haystack integration](https://github.com/deepset-ai/haystack-core-integrations)
- [Haystack documentation](https://docs.haystack.deepset.ai/)

## [Mem0](https://github.com/mem0ai/mem0)

Self-improving memory layer for LLM applications. Valkey serves as the storage backend for user memories, facts, and preferences with native `provider: "valkey"` support.

- [Mem0 Valkey provider documentation](https://docs.mem0.ai/components/vectordbs/config)
- [Mem0 quickstart](https://docs.mem0.ai/getting-started/quickstart)

## [llm-d](https://github.com/llm-d/llm-d)

Kubernetes-native inference platform for LLM serving with state-of-the-art performance. Valkey provides the message queue for asynchronous request processing, using sorted sets for priority-based scheduling.

- [Asynchronous processing guide](https://github.com/llm-d/llm-d/tree/main/guides/asynchronous-processing)

## [LangChain / LangGraph](https://github.com/langchain-ai/langgraph)

Framework for building LLM-powered applications with chains and agents. Valkey provides LLM response caching, vector search, and checkpoint persistence for LangGraph agent workflows.

- [LangChain documentation](https://python.langchain.com/docs/integrations/providers/)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)

## [Strands Agents](https://github.com/strands-agents/sdk-python)

SDK for building AI agents. Valkey provides persistent session storage for conversation history, session metadata, and agent state via the strands-valkey-session-manager package.

- Integration: [strands-valkey-session-manager](https://github.com/jeromevdl/strands-valkey-session-manager)
- [Strands Agents documentation](https://strandsagents.com/latest/)
