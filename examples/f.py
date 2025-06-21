from fntypes import F, Ok

f = F[int]()\
    .then(lambda x: Ok(x))\
    .then(lambda r: r.map_or(0, lambda x: x + 1))\
    .then(lambda r: r.unwrap())

print(f(1))  # 2
