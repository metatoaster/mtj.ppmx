def _simple_form_handle_next(iq, session):
    session['form'] = iq['command']['form']

def add_user(client, accountjid, password, password_verify=None):
    if password_verify is None:
        # well sometimes we really don't care.
        password_verify = password

    # XXX provide error handler method
    session = {'next': _simple_form_handle_next}

    client.plugin['xep_0133'].add_user(session=session, block=True)
    # XXX verify that a form exists.

    form = session['form']
    form['type'] = 'submit'
    form['fields']['accountjid']['value'] = accountjid
    form['fields']['password']['value'] = password
    form['fields']['password-verify']['value'] = password_verify
    session['payload'] = form
    client.plugin['xep_0050'].continue_command(session=session)

    # XXX return result code/msg

def delete_user(client, accountjids):
    if not isinstance(accountjids, list):
        accountjids = [accountjids]
    session = {'next': _simple_form_handle_next}

    client.plugin['xep_0133'].delete_user(session=session, block=True)
    # XXX verify that a form exists.
    form = session['form']
    form['type'] = 'submit'
    form['fields']['accountjids']['value'] = accountjids
    session['payload'] = form
    client.plugin['xep_0050'].continue_command(session=session)

    # XXX return result code/msg
