# resilient-requests
Requests with added support for resilience i.e., automatic retry support on temporary errors like 502, 503, 504 (configurable)

## Usage

```
rs = ResilientSession(max_retries=3)
rs.get('http://httpstat.us/502')
```

## Todo

- [ ] Implement Exponential backoff
- [ ] Add tests

## License
[The MIT License](./LICENSE)