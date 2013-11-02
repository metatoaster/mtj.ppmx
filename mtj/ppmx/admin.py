def add_user(bot, accountjid, password, password_verify=None):
    def handle_next(iq, session):
        session['form'] = iq['command']['form']

    if password_verify is None:
        # well sometimes we really don't care.
        password_verify = password

    session = {'next': handle_next}  # XXX provide error handler method

    bot.client.plugin['xep_0133'].add_user(session=session, block=True)
    # XXX verify that a form exists.

    form = session['form']
    form['fields']['accountjid']['value'] = accountjid
    form['fields']['password']['value'] = password
    form['fields']['password-verify']['value'] = password_verify
    session['payload'] = form
    bot.client.plugin['xep_0050'].continue_command(session=session)

    # XXX return result code/msg

