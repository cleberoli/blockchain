pragma solidity >=0.4.22 <0.6.0;

contract olicoin_ico {

    uint public max_olicoins = 1000000;
    uint public usd_to_olicoins = 1000;
    uint public total_olicoins_bought = 0;

    mapping(address => uint) equity_olicoins;
    mapping(address => uint) equity_usd;

    modifier can_by_olicoins(uint usd_invested) {
        require(usd_invested*usd_to_olicoins + total_olicoins_bought <= max_olicoins);
        _;
    }

    function equity_in_olicoins(address investor) external view returns(uint) {
        return equity_olicoins[investor];
    }

    function equity_in_usd(address investor) external view returns(uint) {
        return equity_usd[investor];
    }

    function buy_olicoins(address investor, uint usd_invested) external can_by_olicoins(usd_invested) {
        uint olicoins_bought = usd_invested*usd_to_olicoins;
        equity_olicoins[investor] += olicoins_bought;
        equity_usd[investor] += usd_invested;
        total_olicoins_bought += olicoins_bought;

    }

    function sell_olicoins(address investor, uint olicoins_sold) external {
        equity_olicoins[investor] -= olicoins_sold;
        equity_usd[investor] -= (olicoins_sold/usd_to_olicoins);
        total_olicoins_bought -= olicoins_sold;

    }

}