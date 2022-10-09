import BigNumber from 'bignumber.js';
import fetch from 'node-fetch';

const calcBptTokenSpotPrice = (sellingToken, buyingToken) => (
    (sellingToken.balance.div(sellingToken.weight)).div((buyingToken.balance).div(buyingToken.weight))
)

const getBalancerPrices = async () => {
    const graphUri = 'https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-arbitrum-v2'
    // 1-BTC/USD and 1-ETH/USD
    const pools = ['0x6ee86e032173716a41818e6d6d320a752176d697', '0x17a35e3d578797e34131d10e66c11170848c6da1']
    // 3-BTC/USD and 3-ETH/USD
    const leveragedPools = [
        '0xcf3ae4b9235b1c203457e472a011c12c3a2fde93',
        '0x996616bde0cb4974e571f17d31c844da2bd177f8',
    ]
    // wETH wBTC USDC pool
    const wPool = '0x64541216bafffeec8ea535bb71fbc927831d0595'
    const data = {
        query: `{
                leveragedPools: pools(where: { 
                    address_in: ${JSON.stringify(leveragedPools)}
                }) {
                    id
                    address
                    tokens {
                        address
                        balance
                        decimals
                        weight
                        symbol
                    }
                },
                nonLeveragedPools: pools(where: { 
                    address_in: ${JSON.stringify(pools)}
                }) {
                    id
                    address
                    tokens {
                        address
                        balance
                        decimals
                        weight
                        symbol
                    }
                },
                wPool: pools(where: {
                    address: "${wPool}"
                }) {
                    id
                    address
                    tokens {
                        address
                        balance
                        decimals
                        weight
                        symbol
                    }
                }

            }`,
    };

    const res = await fetch(graphUri, {
        method: 'POST',
        body: JSON.stringify(data),
    })
        .then((res) => res.json())
        .catch((err) => {
            console.error('Failed to fetch tokens from balancer graph', err);
            return {};
        });
    const tokenPrices = {};
    const getTokenPrices = (pools, baseAssets) => {
        for (const pool of pools) {
            const baseAsset = pool.tokens.filter((token) => baseAssets.includes(token.symbol))[0];
            const poolTokens = pool.tokens.filter((token) => !baseAssets.includes(token.symbol));
            let baseBalance = new BigNumber(baseAsset.balance);
            if (baseAsset.symbol !== 'USDC') {
                baseBalance = baseBalance.times(tokenPrices[baseAsset.symbol]);
            }
            for (const token of poolTokens) {
                tokenPrices[token.symbol] = calcBptTokenSpotPrice(
                    {
                        balance: baseBalance,
                        weight: new BigNumber(baseAsset.weight),
                    },
                    {
                        balance: new BigNumber(token.balance),
                        weight: new BigNumber(token.weight),
                    },
                );
            }
        }
    };
    getTokenPrices(res.data.wPool, ['USDC']);
    getTokenPrices(res.data.nonLeveragedPools, ['USDC']);
    getTokenPrices(res.data.leveragedPools, ['WETH', 'WBTC']);
    Object.keys(tokenPrices).forEach((price) => {
        console.log(`${price} price: $${tokenPrices[price].toNumber()}`)
    })
    return tokenPrices;
};

getBalancerPrices();