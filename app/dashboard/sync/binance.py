import logging

from django.utils import timezone

import requests
from dashboard.sync.helpers import record_payout_activity

logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0. 2272.118 Safari/537.36.'}


def get_binance_txn_status(fulfillment):

    txnid = fulfillment.payout_tx_id
    network = fulfillment.bounty.network if fulfillment.bounty.network else None

    if not txnid:
        return None

    response = {
        'status': 'pending'
    }

    try:
        if network == 'mainnet':
            binance_url = f'https://bsc-dataseed.binance.org'
        else:
            binance_url = f'https://data-seed-prebsc-1-s1.binance.org:8545'

        data = {
            'jsonrpc': '2.0',
            'method': 'eth_getTransactionReceipt',
            'params': [
                txnid
            ],
            'id': 0
        }

        binance_response = requests.post(binance_url, json=data, headers=headers).json()

        result = binance_response['result']

        response = {
            'status': 'pending'
        }

        if result:

            tx_status = int(result.get('status'), 16) # convert hex to decimal

            if tx_status == '1':
                response = {
                    'status': 'done'
                }
            elif tx_status == '0':
                response = {
                    'status': 'expired'
                }
            else:
                replacedTxnId = getReplacedTX(txnid)
                if replacedTxnId:
                    fulfillment.payout_tx_id = replacedTxnId
                    fulfillment.save()
                    response = get_binance_txn_status(fulfillment)

    except Exception as e:
        logger.error(f'error: get_binance_txn_status - {e}')
    finally:
        return response


def sync_binance_payout(fulfillment):
    if fulfillment.payout_tx_id:
        txn_status = get_binance_txn_status(fulfillment)
        if txn_status:
            if txn_status.get('status') == 'done':
                fulfillment.payout_status = 'done'
                fulfillment.accepted_on = timezone.now()
                fulfillment.accepted = True
                record_payout_activity(fulfillment)
            elif txn_status.get('status') == 'expired':
                fulfillment.payout_status = 'expired'

        fulfillment.save()
